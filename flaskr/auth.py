from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import database
from flask_login import login_user, login_required, logout_user, current_user
# from flask_mail import Mail

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta, tente novamente.', category='error')
        else:
            flash('E-mail não inscrito.', category='error')

    return render_template("auth/login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # if database.session.query(User).filter(User.email == email).count() == 0:

        user = User.query.filter_by(email=email).first()
        if user:
            flash('E-mail já inscrito.', category='error')
        elif len(email) < 4:
            flash('O e-mail deve ter mais de 3 caracteres.', category='error')
        elif len(first_name) < 2:
            flash('O nome deve ter mais de 1 caractere.', category='error')
        elif password1 != password2:
            flash('As senhas não coincidem.', category='error')
        elif len(password1) < 7:
            flash('A senha deve ter pelo menos 7 caracteres.', category='error')
        else:
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1, method='sha256'))
            database.session.add(new_user)
            database.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("auth/register.html", user=current_user)
