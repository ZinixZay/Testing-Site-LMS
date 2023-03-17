import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Task(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True)
    question = sqlalchemy.Column(sqlalchemy.String)
    answer = sqlalchemy.Column(sqlalchemy.String)
    addition = sqlalchemy.Column(sqlalchemy.String)

    def to_dict(self):
        res = {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "addition": self.addition
        }
        return res
