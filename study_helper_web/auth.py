from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        acc_name = request.form.get('accName')
        password = request.form.get('password')
        user = User.query.filter_by(acc_name=acc_name).first()
        if user is None:
            flash('User with this account name does not exist', category='error')
        elif not check_password_hash(user.password, password):
            flash('Incorrect password', category='error')
        else:
            flash(f'Welcome back {acc_name}!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
    return render_template('login.html', user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        acc_name = request.form.get('accName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(acc_name=acc_name).first()
        if user:
            flash('This account name already exists', category='error')
        elif acc_name == '':
            flash('Account name should not be empty', category='error')
        elif len(password1) < 5:
            flash('Password length should be at least 5 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        else:
            new_user = User(acc_name=acc_name, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(f'Welcome aboard {acc_name}!', category='success')
            return redirect(url_for('views.home'))
    return render_template('sign_up.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


