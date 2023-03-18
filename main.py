import flask
import os
import dotenv
from lib import login_template
from lib import register_template
from data import db_session
from data.users import User


app = flask.Flask(__name__)
db_session.global_init("db/data.db")
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


@app.route('/')
def index():
    return ''


def create_user(form: dict):
    if not form:
        return

    session = db_session.create_session()
    user = User()
    user.role = form['role']
    user.login = form['login']
    user.hashed_password = form['hashed_password']
    user.email = form['email']

    session.add(user)
    session.commit()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = register_template.RegisterForm()
    if form.validate_on_submit():
        create_user(flask.request.form.to_dict())
        return flask.redirect('/')
    return flask.render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = login_template.LoginForm()
    if form.validate_on_submit():
        return flask.redirect('/')
    return flask.render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    app.run(debug=True, load_dotenv=True)
