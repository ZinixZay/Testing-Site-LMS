import io
import flask
import os
import dotenv
import flask_login
from core import database_functions
from flask_login import current_user

from data import db_session
from data import users
from lib import login_template
from lib import register_template
from lib import search_variant_template
from lib import variant_constructor_template


class AddVariantDataStorage:
    def __init__(self):
        self.json_response = {}
        self.files = None

    def clear(self):
        self.json_response = {}
        self.files = None


app = flask.Flask(__name__)
db_session.global_init("db/data.db")
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

add_variant_data_storage = AddVariantDataStorage()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(users.User).get(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return flask.redirect('/cabinet')
    return flask.redirect('/login')


@app.route('/faq')
def faq():
    return flask.render_template('faq.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return flask.redirect('/')
    form = register_template.RegisterForm()
    if form.validate_on_submit():
        if database_functions.registrate_person(flask.request.form.to_dict()):
            return flask.redirect('/login')
        return flask.render_template('register.html', title='Регистрация', form=form, message="Пользователь с таким "
                                                                                              "логином или почтой уже"
                                                                                              " существует")
    return flask.render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return flask.redirect('/')
    form = login_template.LoginForm()
    if form.validate_on_submit():
        user = database_functions.login_person(flask.request.form.to_dict())
        if user:
            flask_login.login_user(user, remember=form.remember_me.data)
            return flask.redirect('/')
        return flask.render_template('login.html', title='Авторизация', form=form, message="Неверное имя пользователя "
                                                                                           "либо пароль")
    return flask.render_template('login.html', title='Авторизация', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    flask_login.logout_user()
    return flask.redirect('/login')


@app.route('/cabinet', methods=['GET'])
def cabinet():
    if current_user.is_authenticated:
        return flask.render_template('cabinet.html', user=current_user)
    return flask.redirect('/login')


@app.route('/variants', methods=['GET'])
def variants():
    if current_user.is_authenticated:
        vs = database_functions.get_all_variants(current_user)
        return flask.render_template('variants.html', variants=vs)
    else:
        return flask.redirect('/login')


@app.route('/add_variant', methods=['GET', 'POST'])
def add_variant():
    global request_json

    if flask.request.method == 'GET':
        try:
            flask_login.current_user.role
        except AttributeError:
            return 'Вы не залогинены', 400
    if flask.request.method == 'GET' and not flask_login.current_user.role == 'Учитель':
        return 'Вы не учитель', 400

    form = variant_constructor_template.ConstructorForm()
    if flask.request.content_type == "application/json":
        print('application/json!!!')
        add_variant_data_storage.json_response = flask.request.get_json(silent=True)
        return 'None'
    if flask.request.method == "POST" and form.title.validate(form):
        if flask.request.files:
            add_variant_data_storage.files = flask.request.files
        print("response_json:", add_variant_data_storage.json_response)
        print('files:', add_variant_data_storage.files)
    if add_variant_data_storage.json_response:
        database_functions.add_variant(add_variant_data_storage.json_response, add_variant_data_storage.files)

        return flask.redirect('/')

    add_variant_data_storage.clear()
    return flask.render_template('add_variant.html', form=form)


@app.route('/uploads/<filename>')
def return_image(filename: str):
    return flask.send_from_directory('./uploads', filename)


@app.route('/solve_variant/<variant_id>', methods=['GET', 'POST'])
def solve_variant(variant_id: int):
    if flask.request.method == "POST":
        if flask.request.content_type == "application/json":
            print('answer json:', flask.request.get_json(silent=True))
            database_functions.add_answers(flask.request.get_json(silent=True), variant_id)
        secrecy = database_functions.get_variant_secrecy(variant_id)
        if secrecy:
            return flask.redirect(f'/result/{variant_id}')
        return flask.redirect('/')
    if flask.request.method == 'GET':
        tasks = database_functions.get_tasks_by_variant_id(variant_id)
        return flask.render_template('solve_variant.html', tasks=tasks)


@app.route('/search_variant', methods=['GET', 'POST'])
def search_variant():
    form = search_variant_template.SearchForm()
    _variants = []
    if form.validate_on_submit():
        _variants = database_functions.get_variant_by_search_request(flask.request.form.get('search_type'),
                                                                     flask.request.form.get('search_request'))
    return flask.render_template('search_variant.html', form=form, variants=_variants)


@app.route('/result/<variant_id>', methods=['GET'])
def result(variant_id: int):
    if current_user.is_authenticated:
        data = database_functions.compare_variant(variant_id, current_user)
        return flask.render_template('variant_result.html', answers=data)
    return ''


if __name__ == '__main__':
    app.run(debug=True, load_dotenv=True)
