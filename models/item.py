from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class ItemModel(BaseModel):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    price = Column(Float(precision=2), unique=False, nullable=False)

    store_id = Column(Integer, ForeignKey('stores.id'), unique=False, nullable=False)
    store = relationship('StoreModel', back_populates='items')
    tags = relationship('TagModel', back_populates='items', secondary='items_tags')
