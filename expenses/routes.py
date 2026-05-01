from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from action_db import get_user_expenses, add_new_expense, update_user_balance

expenses_bp = Blueprint('expenses', __name__, template_folder='templates')


@expenses_bp.route('/index')
@login_required
def index():
    user_expenses = get_user_expenses(current_user)
    total_spent = sum(e.amount for e in user_expenses)
    remaining = current_user.initial_balance - total_spent

    eur_rate = 0.92
    currency = request.args.get('curr', 'USD')
    display_total = remaining * eur_rate if currency == 'EUR' else remaining

    labels = [e.item for e in user_expenses]
    values = [e.amount for e in user_expenses]

    return render_template('index.html', total=display_total, currency=currency,
                           expenses=user_expenses, labels=labels, values=values,
                           start_bal=current_user.initial_balance)


@expenses_bp.route('/set_balance', methods=['POST'])
@login_required
def set_balance():
    amount = request.form.get('balance')
    if amount:
        update_user_balance(current_user, float(amount))
    return redirect(url_for('expenses.index'))


@expenses_bp.route('/add', methods=['POST'])
@login_required
def add_expense():
    item = request.form.get('item')
    amount = request.form.get('amount')
    category = request.form.get('category')
    if item and amount:
        add_new_expense(item, float(amount), category, current_user)
    return redirect(url_for('expenses.index'))