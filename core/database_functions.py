from data import db_session
from data.users import User


def check_user_exists(login: str, email: str = '') -> bool:
    db_session.global_init("db/data.db")
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.login == login).all() or \
           db_sess.query(User).filter(User.email == email).all()


def registrate_person(person_info: dict) -> bool:
    if check_user_exists(person_info['login'], person_info['email']):
        return False
    else:
        try:
            db_session.global_init("db/data.db")
            db_sess = db_session.create_session()

            user = User(role=person_info['role'],
                        login=person_info['login'],
                        email=person_info['email'])
            user.set_password(person_info['password'])

            db_sess.add(user)
            db_sess.commit()
        except Exception as e:
            print(e)
        return True


def login_person(person_info: dict):
    if check_user_exists(person_info['login']):
        db_session.global_init("db/data.db")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == person_info['login']).first()
        if user.check_passord(person_info['password']):
            return user
    return False
