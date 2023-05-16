import json
import flask_login
import sqlalchemy

from data import db_session
from data import answers
from data import users
from data import variants


def check_user_exists(login: str, email: str = '') -> bool:
    db_session.global_init("db/data.db")
    db_sess = db_session.create_session()
    return db_sess.query(users.User).filter(users.User.login == login).all()


def registrate_person(person_info: dict) -> bool:
    if check_user_exists(person_info['login']):
        return False
    else:
        try:
            db_session.global_init("db/data.db")
            db_sess = db_session.create_session()

            user = users.User(role=person_info['role'],
                              login=person_info['login'],
                              name=person_info['name'],
                              surname=person_info['surname'])
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


def add_variant(json_dict: dict, files):
    if not json_dict:
        return

    db_sess = db_session.create_session()
    print('DB WRITING')

    tasks = json_dict['tasks']
    text_tasks = {index: task for index, task in tasks.items() if task['type'][0] == 'text'}
    paths = []
    try:
        for file in files.getlist('addition'):
            if not file:
                continue
            file_path = './uploads/' + file.filename
            file.save(file_path)
            paths.append(file_path)
        for index, text_task in enumerate(text_tasks.items()):
            try:
                text_task[1]['addition'][0] = paths[index]
                tasks[text_task[0]] = text_task[1]
            except IndexError:
                text_task[1]['addition'][index] = None
            text_task[1]['addition'] = [i for i in text_task[1]['addition'] if i is not None]
        print('tasks:', tasks)
    except AttributeError:
        pass

    variant = variants.Variant()
    variant.secrecy = json_dict['secrecy']
    variant.title = json_dict['title']
    variant.theme = json_dict['theme']
    variant.author_id = flask_login.current_user.id
    variant.task = json.dumps(tasks)

    db_sess.add(variant)
    db_sess.commit()


def get_tasks_by_variant_id(variant_id: int):
    db_sess = db_session.create_session()

    task = json.loads(
        db_sess.query(variants.Variant.task).filter(variants.Variant.id == variant_id).first()[0]
    )
    return task


def add_answers(json_dict: dict, variant_id: int):
    db_sess = db_session.create_session()
    answer = answers.Answer()
    answer.answered_id = flask_login.current_user.id
    answer.variant_id = variant_id
    _answer = {}

    answer.answer = json.dumps(json_dict)

    db_sess.add(answer)
    db_sess.commit()


def get_variant_by_search_request(search_type: str, search_request: str) -> list[variants.Variant]:
    db_sess = db_session.create_session()

    if search_type == 'id':
        variant = db_sess.query(variants.Variant). \
            filter(variants.Variant.id == int(search_request)).first()
        if variant:
            return [variant]
    elif search_type == 'title':
        _variants = db_sess.query(variants.Variant). \
            filter(variants.Variant.title.contains(search_request)).all()
        _variants = [i for i in _variants]
        if _variants:
            return _variants
    elif search_type == 'theme':
        _variants = db_sess.query(variants.Variant). \
            filter(variants.Variant.theme.contains(search_request.lower())).all()
        _variants = [i for i in _variants]
        if _variants:
            return _variants

    return []


def get_answers_by_variant_id(variant_id: int):
    db_sess = db_session.create_session()
    _answers = db_sess.query(answers.Answer). \
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
    return result


def get_all_variants(user):
    db_session.global_init("db/data.db")
    db_sess = db_session.create_session()
    _variants = db_sess.query(variants.Variant).filter(variants.Variant.author_id == user.id).all()
    vrs = list()
    for i in _variants:
        vrs.append(i)
    return vrs


def compare_variant(variant_id, user) -> list:
    results = list()
    db_session.global_init("db/data.db")
    db_sess = db_session.create_session()
    _true_answer = json.loads(
        db_sess.query(variants.Variant.task).filter(variants.Variant.id == variant_id).one()[0]
    )
    _answers = db_sess.query(answers.Answer).filter(answers.Answer.variant_id == variant_id).all()

    if user.role == 'Ученик':  # для ученика получаем последнюю работу
        _answers = [_answers[-1]]

    for ans in _answers:
        name = db_sess.query(users.User.name).filter(users.User.id == ans.answered_id).one()[0]
        surname = db_sess.query(users.User.surname).filter(users.User.id == ans.answered_id).one()[0]
        answer_info = json.loads(
            db_sess.query(answers.Answer.answer).filter(answers.Answer.id == ans.id).one()[0].replace("'", '"')
        )
        result = {'full_name': name + ' ' + surname, 'answers': []}
        for _curr_answer, _curr_login_answer in zip(_true_answer.items(), answer_info.values()):
            if _curr_answer[1]['type'][0] == 'text':
                correctness = None
                showing_answer = _curr_login_answer['answer'][0]
            else:  # if type == 'test'
                _curr_true_answer = _curr_answer[1]['isTrue']
                if _curr_true_answer == _curr_login_answer['answer']:
                    correctness = True
                else:
                    correctness = False
                showing_answer = '    '.join(
                    [_curr_answer[1]['answer'][i]
                     for i in range(len(_curr_answer[1]['answer']))
                     if _curr_login_answer['answer'][i]
                     ]
                )

            result['answers'].append({'question': _curr_answer[1]['question'][0],
                                      'answer': showing_answer,
                                      'is_correct': correctness})
        results.append(result)
    return results


def get_variant_secrecy(variant_id: int):
    db_sess = db_session.create_session()
    return db_sess.query(variants.Variant.secrecy).filter(answers.Answer.id == variant_id).all()
