# from sqlmodel import SQLModel, Field, Relationship # type: ignore
# from datetime import datetime
# from typing import Optional

# class ProductPriceHistory(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     product_id: int = Field(foreign_key="product.id")
#     old_price: float
#     new_price: float
#     timestamp: datetime = Field(default_factory=datetime.utcnow)

#     product: Optional["Product"] = Relationship(back_populates="price_history") 
