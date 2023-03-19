import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Variant(SqlAlchemyBase):
    __tablename__ = 'variants'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True)
    secrecy = sqlalchemy.Column(sqlalchemy.Boolean, default=0)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    theme = sqlalchemy.Column(sqlalchemy.String)
    task_list = sqlalchemy.Column(sqlalchemy.String)

    def to_dict(self):
        res = {
            "id": self.id,
            "secrecy": self.secrecy,
            "author": self.author,
            "identigier": self.identifier,
            "theme": self.theme,
            "task_list": self.task_list
        }
        return res
