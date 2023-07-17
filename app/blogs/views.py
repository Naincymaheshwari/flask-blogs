from datetime import datetime
from flask import jsonify, request, g
from app import db
from app.blogs import blogs_bp
from app.blogs.models import BlogsSchema, Blogs
from lib.jwt_utils import login_required


@blogs_bp.route("/", methods=['GET'])
def get_blogs():
    blogs = db.session.query(Blogs).all()
    return jsonify({"response": "success", "blogs": BlogsSchema().dump(blogs, many=True)}), 200


@blogs_bp.route("/get/<int:blog_id>", methods=['GET'])
def get_blog(blog_id):
    blog = db.session.query(Blogs).filter_by(id=blog_id).first()
    if blog is None:
        return jsonify({"response": "failure", "message": "blog with given Id doesn't exists"}), 404
    return jsonify({"response": "success", "blog": BlogsSchema().dump(blog)}), 200


@blogs_bp.route("/add", methods=['POST'])
@login_required
def add_blog():
    data = request.get_json()
    # Add Validator for validating data
    blog = db.session.query(Blogs).filter_by(title=data['title']).first()
    if blog is not None:
        return jsonify({"response": "failure", "message": "blog already exists with given title"}), 409

    try:
        blog = Blogs(title=data['title'], blog_author=data['blog_author'], description=data['description'], user_id=g.user_id)
        db.session.add(blog)
        db.session.commit()
    except Exception as e:
        print("Exception occurred during saving blog message", str(e))
        raise Exception("Exception occurred during saving blog message")
    return jsonify({"response": "success", "blog": BlogsSchema().dump(blog)}), 200


@blogs_bp.route("/update/<int:blog_id>", methods=['PATCH'])
@login_required
def update_blog(blog_id):
    data = request.get_json()
    blog = db.session.query(Blogs).filter_by(id=blog_id).first()
    if blog is None:
        return jsonify({"response": "failure", "message": "blog doesn't exist"}), 404

    if blog.user_id != g.user_id:
        return jsonify({"response": "failure", "message": "unauthorized access for this blog"}), 403

    try:
        if 'title' in data:
            blog.title = data['title']
        if 'blog_author' in data:
            blog.blog_author = data['blog_author']
        if 'description' in data:
            blog.description = data['description']
        blog.updated_at = datetime.utcnow()
        db.session.add(blog)
        db.session.commit()
    except Exception as e:
        print("Exception occurred during updating blog message", str(e))
        raise Exception("Exception occurred during updating blog message")
    return jsonify({"response": "success", "blog": BlogsSchema().dump(blog)}), 200


@blogs_bp.route("/delete/<int:blog_id>", methods=['DELETE'])
@login_required
def delete_blog(blog_id):
    blog = db.session.query(Blogs).filter_by(id=blog_id).first()
    if blog is None:
        return jsonify({"response": "failure", "message": "blog doesn't exist"}), 404

    if blog.user_id != g.user_id:
        return jsonify({"response": "failure", "message": "unauthorized access for this blog"}), 403

    try:
        db.session.delete(blog)
        db.session.commit()
    except Exception as e:
        print("Exception occurred during deleting blog message", str(e))
        raise Exception("Exception occurred during deleting blog message")
    return jsonify({"response": "success", "message": "Blog deleted successfully"}), 200
