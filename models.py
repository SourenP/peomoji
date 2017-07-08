from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """ Define a base way to jsonify models, dealing
        with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class Emojis(BaseModel, db.Model):
    """Model for the emojis table"""
    __tablename__ = 'emojis'

    id = db.Column(db.Integer, primary_key = True)
    emoji = db.Column(db.VARCHAR(1), nullable=False)
    text = db.Column(db.TEXT)
    author = db.Column(db.TEXT)
    datetime = db.Column(db.DATETIME, nullable=False)
