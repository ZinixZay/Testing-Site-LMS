import flask
import os
import dotenv
from lib import login_template
from data import db_session


app = flask.Flask(__name__)
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db_session.global_init("db/data.db")


@app.route('/')
def index():
    return ''


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = login_template.LoginForm()
    if form.validate_on_submit():
        return flask.redirect('/')
    return flask.render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    app.run(debug=True, load_dotenv=True)
