import flask
import os
import dotenv
import flask_login
from lib import login_template
from lib import register_template
from data import db_session
from core.database_functions import registrate_person, login_person
from data.users import User
from flask_login import current_user


app = flask.Flask(__name__)
db_session.global_init("db/data.db")
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return f'Пользователь зареган. login - {current_user.login}'
    return 'Пользователь не зареган'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return flask.redirect('/')
    form = register_template.RegisterForm()
    if form.validate_on_submit():
        if registrate_person(flask.request.form.to_dict()):
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
        user = login_person(flask.request.form.to_dict())
        if user:
            flask_login.login_user(user, remember=form.remember_me.data)
            return
        return flask.render_template('login.html', title='Авторизация', form=form, message="Неверное имя пользователя "
                                                                                           "либо пароль")
    return flask.render_template('login.html', title='Авторизация', form=form)


@app.route('/add_variant', methods=['GET', 'POST'])
def add_variant():
    if flask.request.method == 'POST':

        print(flask.request.form)
        return flask.redirect('/')
    else:
        return flask.render_template('add_variant.html')


if __name__ == '__main__':
    app.run(debug=True, load_dotenv=True)
