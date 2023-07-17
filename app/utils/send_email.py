from flask import current_app
from flask_mail import Message
from app import mail


def send_email(email, subject, content):
    msg = Message(subject, sender=current_app.config['MAIL_USERNAME'], recipients=[email])
    msg.html = content
    mail.send(msg)
