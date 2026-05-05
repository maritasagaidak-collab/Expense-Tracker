from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from action_db import create_user, get_user_by_username

auth_bp = Blueprint('auth', __name__, template_folder='templates')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 1. Валідація: перевірка на порожні поля
        if not username or not password:
            flash("Будь ласка, заповніть усі поля!", "error")
            return redirect(url_for('auth.register'))

        # 2. Перевірка: чи не зайнятий логін
        if get_user_by_username(username):
            flash("Цей логін уже зайнятий. Спробуйте інший!", "error")
            return redirect(url_for('auth.register'))

        # 3. Створення користувача
        try:
            create_user(username, password)
            flash("Акаунт успішно створено! Тепер увійдіть.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash("Помилка при створенні акаунту. Спробуйте пізніше.", "error")

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = get_user_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('expenses.index'))
        else:
            flash("Невірний логін або пароль!", "error")

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))