import bcrypt
import datetime as dt
from mongoengine import Document, StringField, EmailField, DateTimeField


class User(Document):
    ROLE_CHOICES = ("staff", "patient")

    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)
    name = StringField(required=True, max_length=120)
    phone = StringField(max_length=20)
    role = StringField(choices=ROLE_CHOICES, default="patient")
    created_at = DateTimeField(default=dt.datetime.utcnow)

    meta = {"collection": "users"}

    def set_password(self, raw_password):
        self.password_hash = bcrypt.hashpw(
            raw_password.encode(), bcrypt.gensalt()
        ).decode()

    def check_password(self, raw_password):
        return bcrypt.checkpw(
            raw_password.encode(), self.password_hash.encode()
        )
