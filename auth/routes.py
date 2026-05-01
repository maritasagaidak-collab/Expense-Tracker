from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from action_db import create_user, get_user_by_username

auth_bp = Blueprint('auth', __name__, template_folder='templates')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if get_user_by_username(username):
            return "Користувач вже існує! Використовуйте інший логін."

        create_user(username, password)
        return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_user_by_username(request.form.get('username'))
        if user and user.check_password(request.form.get('password')):
            login_user(user)
            return redirect(url_for('expenses.index'))
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))