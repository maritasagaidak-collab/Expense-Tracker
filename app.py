#EXPENSE TRACKER!!!
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from models import User, db
from auth.routes import auth_bp
from expenses.routes import expenses_bp
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_key_123'

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(expenses_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

@app.route('/')
def start():
    return redirect(url_for('auth.login'))

@app.before_request
def before_request():
    db.connect(reuse_if_open=True)

@app.after_request
def after_request(response):
    db.close()
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))