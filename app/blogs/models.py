from datetime import datetime
from marshmallow import Schema, fields
from app import db


class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    blog_author = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class BlogsSchema(Schema):
    class Meta:
        model = Blogs

    id = fields.String(dump_only=True)
    title = fields.String()
    blog_author = fields.String()
    created_at = fields.DateTime()
    description = fields.String()
    user_id = fields.Integer()

