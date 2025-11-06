from sqlmodel import SQLModel, Relationship, Field # type: ignore
from typing import List, Optional
from datetime import datetime, timezone

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    price: Optional[float] = None
    rating: Optional[float] = None
    product_url: str
    image_url: Optional[str] = None
    source: Optional[str] = "amazon"
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    product_url:str = Field(unique=True)

