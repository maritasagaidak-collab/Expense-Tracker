from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from action_db import get_user_expenses, add_new_expense, update_user_balance

expenses_bp = Blueprint('expenses', __name__, template_folder='templates')


@expenses_bp.route('/index')
@login_required
def index():
    currency = request.args.get('curr', 'USD')
    user_expenses = get_user_expenses(current_user)
    total_spent = sum(e.amount for e in user_expenses)
    remaining = current_user.initial_balance - total_spent

    eur_rate = 0.92
    display_total = remaining * eur_rate if currency == 'EUR' else remaining

    return render_template('index.html', total=display_total, currency=currency,
                           labels=[e.item for e in user_expenses],
                           values=[e.amount for e in user_expenses],
                           start_bal=current_user.initial_balance)


@expenses_bp.route('/add_income', methods=['POST'])
@login_required
def add_income():
    try:
        amount = float(request.form.get('amount'))
        if amount <= 0: raise ValueError
        add_new_expense("Дохід", -amount, "Дохід", current_user)
    except:
        flash("Введіть коректну суму!")
    return redirect(url_for('expenses.index'))


@expenses_bp.route('/add', methods=['POST'])
@login_required
def add_expense():
    try:
        amount = float(request.form.get('amount'))
        if amount <= 0: raise ValueError
        add_new_expense(request.form.get('item'), amount, request.form.get('category'), current_user)
    except:
        flash("Помилка в даних витрати!")
    return redirect(url_for('expenses.index'))


@expenses_bp.route('/set_balance', methods=['POST'])
@login_required
def set_balance():
    try:
        update_user_balance(current_user, float(request.form.get('balance', 0)))
    except:
        flash("Некоректний капітал!")
    return redirect(url_for('expenses.index'))