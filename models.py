import bcrypt

from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin

from app import app

from time import time
import jwt

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)

    login = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)

    name = db.Column(db.String(60))
    telephoneNumber = db.Column(db.String(12))

    def __repr__(self):
        return "<{}: {}>".format(self.id, self.login)


    def set_password(self, password):
        # self.password_hash = generate_password_hash(password)
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


    def check_password(self, password):
        # return check_password_hash(self.password_hash, password)
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))


    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')


    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
