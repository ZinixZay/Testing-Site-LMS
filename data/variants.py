import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Variant(SqlAlchemyBase):
    __tablename__ = 'variants'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True)
    secrecy = sqlalchemy.Column(sqlalchemy.Boolean, default=0)
    title = sqlalchemy.Column(sqlalchemy.String)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    theme = sqlalchemy.Column(sqlalchemy.String)
    task = sqlalchemy.Column(sqlalchemy.String)

    def to_dict(self):
        res = {
            "id": self.id,
            "secrecy": self.secrecy,
            "author": self.author,
            "title": self.title,
            "theme": self.theme,
            "task_list": self.task_list
        }
        return res
