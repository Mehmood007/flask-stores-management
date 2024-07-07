from sqlalchemy import Column, ForeignKey, Integer

from models.base_model import BaseModel


class ItemTag(BaseModel):
    __tablename__ = 'items_tags'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), unique=False, nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id'), unique=False, nullable=False)
