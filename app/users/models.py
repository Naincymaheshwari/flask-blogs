from marshmallow import fields, Schema
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(128), nullable=False)
    blogs = db.relationship('Blogs', backref='author', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class UserSchema(Schema):
    class Meta:
        model = Users

    id = fields.String(load_only=True)
    name = fields.String()
    email = fields.String()
    password = fields.String(load_only=True)
