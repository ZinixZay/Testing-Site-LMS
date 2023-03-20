import flask
import os
import sqlalchemy
import flask_login
import data


def check_user_exists(login: str, email: str = '') -> bool:
    data.db_session.global_init("db/data.db")
    db_sess = data.db_session.create_session()
    return db_sess.query(data.users.User).filter(data.users.User.login == login).all() or \
           db_sess.query(data.users.User).filter(data.users.User.email == email).all()


def registrate_person(person_info: dict) -> bool:
    if check_user_exists(person_info['login'], person_info['email']):
        return False
    else:
        try:
            data.db_session.global_init("db/data.db")
            db_sess = data.db_session.create_session()

            user = data.users.User(role=person_info['role'],
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
        data.db_session.global_init("db/data.db")
        db_sess = data.db_session.create_session()
        user = db_sess.query(data.users.User).filter(data.users.User.login == person_info['login']).first()
        if user.check_passord(person_info['password']):
            return user
    return False


def add_task(task_info: dict) -> bool:
    try:
        db_session = data.db_session.create_session()
        task = data.tasks.Task(question=task_info['question'],
                    answer=task_info['answer'],
                    addition=task_info['addition'])

        db_session.add(task)
        db_session.commit()
    except Exception:
        return False
    return True


def add_variant(form, files):
    db_session = data.db_session.create_session()

    previous_task_id = db_session.query(sqlalchemy.func.max(data.tasks.Task.id)).first()[0]
    if not previous_task_id:
        previous_task_id = 0
    print(previous_task_id)

    tasks = []
    task_keys = ['question', 'answer']
    for key in task_keys:
        tasks.append(form.getlist(key))
    paths = ["" for _ in range(len(files.getlist('addition')))]
    for index, file in enumerate(files.getlist('addition')):
        if not file:
            continue
        file_path = './uploads/' + file.filename
        file.save(file_path)
        paths[index] = file_path
    tasks.append(paths)
    tasks = list(zip(*tasks))

    variant = data.variants.Variant()
    variant.secrecy = True if form.get('secrecy') == 'on' else False
    variant.title = form.get('title')
    variant.theme = form.get('theme')
    variant.author_id = flask_login.current_user.id
    variant.task_list = ', '.join([str(previous_task_id + 1 + i) for i in range(len(tasks))])

    db_session.add(variant)
    db_session.commit()

    for task in tasks:
        add_task({'question': task[0],
                  'answer': task[1],
                  'addition': task[2]})
