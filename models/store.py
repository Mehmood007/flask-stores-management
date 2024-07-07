from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class StoreModel(BaseModel):
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    items = relationship(
        'ItemModel', back_populates='store', lazy='dynamic', cascade='all, delete'
    )
    tags = relationship('TagModel', back_populates='stores', lazy='dynamic')
