from playwright.sync_api import sync_playwright # type: ignore
from bs4 import BeautifulSoup   # type: ignore
import re
import time
import random
from typing import List
from models.productModel import Product
from urllib.parse import urljoin

USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/121.0 Safari/537.36")

def _extract_from_html(html: str, base_url: str = "https://www.amazon.com") -> List[dict]:
    soup = BeautifulSoup(html, "html.parser")
    results = []

    # that is the main container for each product
    containers = soup.select("div[data-component-type='s-search-result']") or soup.select(".s-result-item")

    for c in containers:
        title = None
        product_url = None

        # Title & URL patterns
        a_tag = c.select_one("a:has(h2)") or c.select_one("h2 a") or c.select_one("a[href*='/dp/'], a[href*='/gp/']")
        if a_tag:
            span = a_tag.select_one("span") or a_tag.select_one("h2 span")
            title = span.get_text(strip=True) if span else a_tag.get_text(strip=True)
            href = a_tag.get("href")
            product_url = urljoin(base_url, href) if href else None

        # Image
        img = c.select_one("img.s-image")
        image_url = img.get("src") if img and img.get("src") else None

        # Price
        price = None

        # Try normal a-offscreen price (most reliable)
        price_block = c.select_one(".a-price .a-offscreen")
        if price_block:
            price_text = price_block.get_text(strip=True)
            price_str = re.sub(r"[^\d.,]", "", price_text)
            try:
                price = float(price_str.replace(",", ""))
            except:
                price = None

        # Fallback: build from split parts (.a-price-whole + .a-price-fraction)
        if price is None:
            whole = c.select_one(".a-price-whole")
            fraction = c.select_one(".a-price-fraction")
            if whole:
                whole_str = re.sub(r"[^\d]", "", whole.get_text(strip=True))
                fraction_str = re.sub(r"[^\d]", "", fraction.get_text(strip=True)) if fraction else "00"
                try:
                    price = float(f"{whole_str}.{fraction_str}")
                except:
                    price = None

        # Final fallback: any other visible .a-offscreen inside
        if price is None:
            alt_price = c.select_one("span.a-offscreen")
            if alt_price:
                price_str = re.sub(r"[^\d.,]", "", alt_price.get_text(strip=True))
                try:
                    price = float(price_str.replace(",", ""))
                except:
                    price = None
        # Rating
        rating = None
        rating_tag = c.select_one("span.a-icon-alt")
        if rating_tag:
            try:
                rating = float(rating_tag.get_text(strip=True).split()[0].replace(",", "."))
            except:
                rating = None

        if title and product_url:
            results.append({
                "title": title,
                "price": price,
                "rating": rating,
                "product_url": product_url,
                "image_url": image_url
            })

    return results


def scrape_amazon_search(query_or_url: str, max_pages: int = 2):
   
    results = []
    delay_range = (3.0, 7.0)  

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=USER_AGENT)
        page = context.new_page()

        # build URL if a query is provided
        if query_or_url.startswith("http"):
            url = query_or_url
        else:
            q = query_or_url.replace(" ", "+")
            url = f"https://www.amazon.com/s?k={q}"

        page.goto(url, wait_until= "load")
        time.sleep(random.uniform(*delay_range))

        for page_count in range(max_pages):
            html = page.content()
            page_results = _extract_from_html(html, base_url="https://www.amazon.com")
            for r in page_results:
                prod = Product(
                    title=r["title"],
                    price=r["price"],
                    rating=r["rating"],
                    product_url=r["product_url"],
                    image_url=r["image_url"]
                )
                results.append(prod)

            # navigate to next page
            next_btn = page.query_selector("li.a-pagination-item") or page.query_selector("a.s-pagination-next")
            if next_btn:
                try:
                    next_btn.click()
                    time.sleep(random.uniform(*delay_range))
                    page.wait_for_load_state("networkidle", timeout=10000)
                except:
                    break
            else:
                break

        browser.close()

    return results
