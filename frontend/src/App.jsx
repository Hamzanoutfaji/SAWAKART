import { useEffect, useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import api from "./api";
import ProductTable from "./components/ProductTable";
import logo from "./assets/Logo.png";

export default function App() {
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState("");

  const handleScrape = async () => {
    const query = prompt("Enter product search query or URL:");
    if (!query) return;

    const maxPages = parseInt(prompt("Enter max pages to scrape (default 2):") || "2");

    setIsLoading(true);
    setLoadingMessage(`Scraping products for "${query}"...`);

    try {
      const res = await api.post("/scrape", {
        query,
        max_pages: maxPages,
      });

      alert(`Scraped ${res.data.length} products for "${query}"`);
      loadProducts();
    } catch (err) {
      console.error(err);
      alert("Error scraping products. Check console for details.");
    } finally {
      setIsLoading(false);
      setLoadingMessage("");
    }
  };

  const loadProducts = async () => {
    try {
      const res = await api.get("/products/");
      setProducts(res.data);
    } catch (err) {
      console.error(err);
      alert("Error loading products. Check console for details.");
    }
  };

  const downloadCSV = () => {
    if (products.length === 0) {
      alert("No products to download");
      return;
    }
    const headers = Object.keys(products[0]);
    
    // Create CSV header row
    const csvHeader = headers.join(",");
    
    // Create CSV data rows
    const csvRows = products.map(product => {
      return headers.map(header => {
        const value = product[header];
        // Handle values that might contain commas or quotes
        const stringValue = String(value ?? "");
        if (stringValue.includes(",") || stringValue.includes('"') || stringValue.includes("\n")) {
          return `"${stringValue.replace(/"/g, '""')}"`;
        }
        return stringValue;
      }).join(",");
    });
    
    // Combine header and rows
    const csvContent = [csvHeader, ...csvRows].join("\n");
    
    // Create blob and download
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    
    link.setAttribute("href", url);
    link.setAttribute("download", `products_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = "hidden";
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  useEffect(() => {
    loadProducts();
  }, []);

  const handleDelete = (id) => {
    setProducts(products.filter((p) => p.id !== id));
  };

  return (
    <div className="p-4">
      <div className="d-flex justify-content-center mb-4">
        <img src={logo} alt="Sawakart Logo" style={{ height: "80px" }} />
      </div>

      {isLoading && (
        <div className="alert alert-info d-flex align-items-center gap-2 mb-3">
          <div className="spinner-border spinner-border-sm" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <span>{loadingMessage}</span>
        </div>
      )}

      <div className="mb-3 d-flex gap-2">
        <button 
          className="p-button p-component p-button-primary" 
          onClick={handleScrape}
          disabled={isLoading}
        >
          {isLoading ? "Scraping..." : "Scrape Products"}
        </button>
        <button 
          className="p-button p-component p-button-success" 
          onClick={downloadCSV}
          disabled={products.length === 0 || isLoading}
        >
          Download CSV
        </button>
      </div>

      <ProductTable products={products} onDelete={handleDelete} />
    </div>
  );
}