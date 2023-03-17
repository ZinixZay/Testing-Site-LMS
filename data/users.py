import sqlalchemy
from sqlalchemy import orm
from db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True)
    role = sqlalchemy.Column(sqlalchemy.String)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    variants = orm.relationship("Variants", back_populates='user')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_passord(self, password):
        return check_password_hash(self.hashed_password, password)

    def to_dict(self):
        res = {
            "id": self.id,
            "role": self.role,
            "login": self.login,
            "email": self.email
        }
        return res
