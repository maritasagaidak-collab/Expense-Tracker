from models import User, Expense

def create_user(username, password):
    user = User(username=username)
    user.set_password(password)
    user.save()
    return user

def update_user_balance(user, amount):
    user.initial_balance = amount
    user.save()

def get_user_by_username(username):
    return User.get_or_none(User.username == username)

def get_user_expenses(user):
    return Expense.select().where(Expense.user == user)

def add_new_expense(item, amount, category, user):
    return Expense.create(item=item, amount=amount, category=category, user=user)