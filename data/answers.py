import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
import json


class Answer(SqlAlchemyBase):
    __tablename__ = 'answers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True)
    answered_id = orm.relationship(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    variant_id = orm.relationship(sqlalchemy.Integer, sqlalchemy.ForeignKey('variants.id'))
    answer = sqlalchemy.Column(sqlalchemy.String)
    user = orm.relationship('User')
    variant = orm.relationship('Variant')

    def to_dict(self):
        res = {
            "id": self.id,
            "answered_id": self.answered_id,
            "variant_id": self.variant_id,
            "answer": json.loads(self.answer)
        }
        return res
