from fastapi import FastAPI, HTTPException, Depends
from typing import List, Optional
from sqlmodel import Session 
from database import create_db_and_tables, get_session
from models.productModel import Product
from controllers.scraper import scrape_amazon_search
from controllers.crud import list_products, delete_product, save_products
from pydantic import BaseModel 
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI(title="Amazon Scraper Prototype")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Scrape products

class ScrapeRequest(BaseModel):
    query: str
    max_pages: Optional[int] = 1

@app.post("/scrape", response_model=List[Product])
def post_scrape(request: ScrapeRequest, session: Session = Depends(get_session)):
    try:
        scraped = scrape_amazon_search(request.query, max_pages=request.max_pages)
        if not scraped:
            return []
        saved = save_products(session, scraped)
        return saved
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all products 
@app.get("/products", response_model=List[Product])
def get_products(session: Session = Depends(get_session), limit: Optional[int] = 100):
    return list_products(session, limit)


# Delete a product by ID
@app.delete("/products/{product_id}")
def del_product(product_id: int, session: Session = Depends(get_session)):
    ok = delete_product(session, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return {"message": "deleted"}
