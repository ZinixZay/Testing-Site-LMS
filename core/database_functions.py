import json
import flask_login
from data import db_session
from data import answers
from data import users
from data import variants


def check_user_exists(login: str, email: str = '') -> bool:
    db_session.global_init("db/data.db")
    db_sess = db_session.create_session()
    return db_sess.query(users.User).filter(users.User.login == login).all() or \
           db_sess.query(users.User).filter(users.User.email == email).all()


def registrate_person(person_info: dict) -> bool:
    if check_user_exists(person_info['login'], person_info['email']):
        return False
    else:
        try:
            db_session.global_init("db/data.db")
            db_sess = db_session.create_session()

            user = users.User(role=person_info['role'],
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
        user = db_sess.query(users.User).filter(users.User.login == person_info['login']).first()
        if user.check_passord(person_info['password']):
            return user
    return False


def add_variant(form, files):
    db_sess = db_session.create_session()

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

    task_info = dict()
    for i in range(len(tasks)):
        task_info[i] = {'question': tasks[i][0],
                        'answer': tasks[i][1],
                        'addition': tasks[i][2]}
    task_info = json.dumps(task_info)

    variant = variants.Variant()
    variant.secrecy = True if form.get('secrecy') == 'on' else False
    variant.title = form.get('title')
    variant.theme = form.get('theme')
    variant.author_id = flask_login.current_user.id
    variant.task_list = task_info

    db_sess.add(variant)
    db_sess.commit()


def get_tasks_by_variant_id(variant_id: int):
    db_sess = db_session.create_session()

    task = json.loads(
        db_sess.query(variants.Variant.task).filter(variants.Variant.id == variant_id).first()[0]
    )
    return task


def add_answers(form, variant_id: int):
    db_sess = db_session.create_session()

    for index, answer_text in enumerate(form.getlist('answer')):
        answer = answers.Answer()
        answer.answered_id = flask_login.current_user.id
        answer.variant_id = variant_id
        answer.task_id = index + 1
        answer.answer = answer_text

        db_sess.add(answer)
    db_sess.commit()


def get_variant_by_search_request(search_type: str, search_request: str) -> list[variants.Variant]:
    db_sess = db_session.create_session()

    if search_type == 'id':
        variant = db_sess.query(variants.Variant).\
            filter(variants.Variant.id == int(search_request)).first()
        if variant:
            return [variant]
    elif search_type == 'title':
        _variants = db_sess.query(variants.Variant).\
            filter(variants.Variant.title.contains(search_request)).all()
        _variants = [i for i in variants]
        if _variants:
            return _variants
    elif search_type == 'theme':
        _variants = db_sess.query(variants.Variant).\
            filter(variants.Variant.theme.contains(search_request.lower())).all()
        _variants = [i for i in variants]
        if _variants:
            return _variants

    return []


def get_answers_by_variant_id(variant_id: int):
    db_sess = db_session.create_session()
    _answers = db_sess.query(answers.Answer).\
        filter(answers.Answer.id == variant_id,
               answers.Answer.answered_id == flask_login.current_user.id).all()
    tasks = json.loads(
        db_sess.query(variants.Variant.task).filter(variants.Variant.id == variant_id).first()[0]
    )

    result = []
    for answer, task in zip(_answers, tasks.values()):
        result.append({'answer_id': answer.id,
                       'answer': answer.answer,
                       'is_correct': answer.answer.lower() == task['answer'].lower()})
    print(result)
    return result
