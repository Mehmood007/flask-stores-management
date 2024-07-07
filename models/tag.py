from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class TagModel(BaseModel):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)

    stores = relationship('StoreModel', back_populates='tags')
    items = relationship('ItemModel', back_populates='tags', secondary='items_tags')
