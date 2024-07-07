from db import db


class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )
