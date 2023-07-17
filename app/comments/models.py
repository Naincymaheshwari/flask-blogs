from datetime import datetime
from marshmallow import Schema, fields
from app import db


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class CommentsSchema(Schema):
    class Meta:
        model = Comments

    id = fields.String(dump_only=True)
    blog_id = fields.Integer()
    comment = fields.String()
    created_at = fields.DateTime()
    user_id = fields.Integer()
