from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

import logging
logging.basicConfig(level=logging.DEBUG)

def main():
    logging.debug('Debug')
    logging.info('Info')
    logging.warning('Warning')
    logging.error('Error')
    logging.critical('Critical or Fatal')
    # db_session.global_init("db/blogs.db")
    # user = User()
    # user.name = "Пользователь 1"
    # user.about = "биография пользователя 1"
    # user.email = "email@email.ru"
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()

    # app.run()


if __name__ == '__main__':
    main()