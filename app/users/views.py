from datetime import datetime

from flask import request, jsonify, g
from app import db
from app.users import users_bp
from app.users.models import Users, UserSchema
from app.utils.send_email import send_email
from app.utils.utils import password_generator
from lib.jwt_utils import create_token, login_required


@users_bp.route("/signup", methods=['POST'])
def signup():
    # validate_request(data)
    data = request.get_json()
    user = db.session.query(Users).filter(Users.email.ilike(data.get('email'))).first()
    if user is not None:
        raise Exception("Email Id is already registered!")

    try:
        user = Users()
        user.name = data['name']
        user.email = data['email'].lower()
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print("Failed saving user's data", str(e))
        raise Exception("Failed saving user's data")

    return jsonify({
        "response": "success",
        "user": UserSchema().dump(user),
        "token": create_token(user)
    }), 200


@users_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    # validate data
    user = db.session.query(Users).filter(Users.email.ilike(data['email'])).first()
    if user is None:
        raise Exception("Email Id doesn't exists!")

    if not user.check_password(data['password']):
        raise Exception("Incorrect password")

    return jsonify({
        "response": "success",
        "user": UserSchema().dump(user),
        "token": create_token(user)
    }), 200


@users_bp.route("/change-password", methods=['POST'])
@login_required
def update_password():
    data = request.get_json()
    # validate data
    user = db.session.query(Users).filter(Users.email.ilike(g.get('user_email'))).first()
    if not user.check_password(data['old_password']):
        raise Exception("Incorrect password")

    try:
        user.set_password(data['new_password'])
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print("Failed updating user's password", str(e))
        raise Exception("Failed updating user's password")
    return jsonify({
        "response": "success",
        "message": "password changed successfully"
    }), 200


@users_bp.route("/update-profile", methods=['POST'])
@login_required
def update_user():
    data = request.get_json()
    # validate data
    user = db.session.query(Users).filter(Users.email.ilike(g.get('user_email'))).first()
    if user is None:
        raise Exception("User doesn't exist")
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    user.updated_at = datetime.utcnow()
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print("Failed updating user's profile", str(e))
        raise Exception("Failed updating user's profile")
    return jsonify({
        "response": "success",
        "message": "user profile updated successfully"
    }), 200


@users_bp.route("/forgot-password", methods=['POST'])
def forgot_password():
    data = request.get_json()
    # validate data
    user = db.session.query(Users).filter(Users.email.ilike(data['email'])).first()
    if user is None:
        return jsonify({"response": "failure", "message": "user doesn't exists with given email"}), 404

    password = password_generator()
    user.set_password(password)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print("Failed updating user's password", str(e))
        raise Exception("Failed updating user's password")
    message = f"<p>Hi User</p><p>Your new password is {password}</p>"
    send_email(user.email, "Password reset request", message)
    return jsonify({
        "response": "success",
        "message": "New password has been sent on your email"
    }), 200
