from flask import Flask, redirect, url_for
from flask_login import LoginManager
from models import User, db
from auth.routes import auth_bp
from expenses.routes import expenses_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(expenses_bp)

@app.route('/')
def start():
    return redirect(url_for('auth.login'))

@app.before_request
def before_request(): db.connect(reuse_if_open=True)

@app.after_request
def after_request(res):
    db.close()
    return res

if __name__ == '__main__':
    app.run(debug=True)