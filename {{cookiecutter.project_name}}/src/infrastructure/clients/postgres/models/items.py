from sqlalchemy import Column, String, Integer, BigInteger

from .base import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(String(2048))
    price = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Item(resource_id={self.id}, name={self.name})"
