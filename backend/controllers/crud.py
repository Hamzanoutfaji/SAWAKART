from sqlmodel import Session, select # type: ignore
from models.productModel import Product

def save_products(session: Session, products: list[Product]):
    session.add_all(products)
    session.commit()
    for p in products:
        session.refresh(p)
    return products

def list_products(session: Session, limit: int = 100):
    return session.exec(select(Product).order_by(Product.id.desc()).limit(limit)).all()


def delete_product(session: Session, product_id: int):
    p = session.get(Product, product_id)
    if not p:
        return False
    session.delete(p)
    session.commit()
    return True

