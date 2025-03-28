from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Модель пользователя
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Форма авторизации
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Маршрут для авторизации
@app.route('/')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Здесь должна быть логика проверки пользователя
        # Например, проверка в базе данных
        if form.username.data == 'admin' and form.password.data == 'password':
            user = User(1)  # Загружаем пользователя
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

# Маршрут для выхода
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Маршрут для защищенной страницы
@app.route('/dashboard')
@login_required
def dashboard():
    return 'Welcome to Mars One Dashboard!'

if __name__ == '__main__':
    user = User()
    user.name = "Пользователь 1"
    user.about = "биография пользователя 1"
    user.email = "email@email.ru"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()

    # app.run(port=8080, host='127.0.0.1')