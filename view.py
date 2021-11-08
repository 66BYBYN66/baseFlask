from flask import render_template
from flask import redirect
from flask import url_for

from flask_mail import Mail
from flask_mail import Message

from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import current_user
from flask_login import logout_user

from forms import RegisterForm
from forms import LoginForm
from forms import RecoveryPassword
from forms import ResetPassword

from models import db
from models import User

from app import app

from config import host

mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


def create_user(login, email, password):
    usr = User(login=login, email=email)
    usr.set_password(password)
    db.session.add(usr)
    db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('start_page'))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            print('user login')
            login_user(user)
            return redirect(url_for('start_page'))
        else:
            print('not login')
            return redirect(url_for('login'))

    return render_template('loginUsr.html', form=form, usr=current_user)


@app.route('/register', methods=['POST', 'GET'])
def reg_usr():
    if current_user.is_authenticated:
        return redirect(url_for('start_page'))

    form = RegisterForm()

    if form.validate_on_submit():
        login = form.login.data
        email = form.email.data
        password = form.password.data

        checkUniqueLogin = db.session.query(User).filter(User.login == form.login.data).first()

        checkUniqueEmail = db.session.query(User).filter(User.email == form.email.data).first()

        if checkUniqueLogin or checkUniqueEmail:
            return redirect(url_for('reg_usr'))

        create_user(login, email, password)

        print('reg new user')
        return redirect(url_for('start_page'))
    else:
        print("not validate")

    return render_template('regUsr.html', form=form, usr=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('start_page'))


@app.route('/recoveryPassword', methods=['POST', 'GET'])
def recovery():

    form = RecoveryPassword()

    notFindEmail = False
    sendMessage = False

    usr = db.session.query(User).filter(User.email == form.email.data).first()

    if form.validate_on_submit():
        print("validate: ", form.email.data)
        if usr:
            print('find user')
            sendMessage = True
            msg = Message("CODE", recipients=[usr.email], sender=app.config['MAIL_USERNAME'])
            uniqueLink = url_for('reset_password', token=usr.get_reset_password_token(), _external=True)

            msg.body = "Перейдите по этой ссылке для восстановления пароля {}".format(uniqueLink)
            mail.send(msg)
        else:
            notFindEmail = True
            print('not find user')
    else:
        print("not validate: ", form.email.data)

    return render_template('recoveryPassword.html', form=form, sendMsg=sendMessage, invalidEmail=notFindEmail)


@app.route('/reset/<token>', methods=['POST', 'GET'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('start_page'))

    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('start_page'))

    form = ResetPassword()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)


@app.route("/", methods=['POST', 'GET'])
def start_page():

    return render_template("startPage.html")
