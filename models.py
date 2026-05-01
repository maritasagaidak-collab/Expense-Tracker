from peewee import *
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SqliteDatabase('expenses_v2.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel, UserMixin):
    username = CharField(unique=True)
    password_hash = CharField()
    initial_balance = FloatField(default=0.0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Expense(BaseModel):
    item = CharField()
    amount = FloatField()
    category = CharField()
    user = ForeignKeyField(User, backref='expenses')

db.connect()
db.create_tables([User, Expense])