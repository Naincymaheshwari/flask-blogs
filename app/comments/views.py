from datetime import datetime
from flask import jsonify, request, g
from app import db
from app.blogs.models import Blogs
from app.comments import comments_bp
from app.comments.models import Comments, CommentsSchema
from lib.jwt_utils import login_required


@comments_bp.route("/<int:blog_id>/comments", methods=['GET'])
def get_blog_comments(blog_id):
    comments = db.session.query(Comments).filter_by(blog_id=blog_id).all()
    return jsonify({"response": "success", "comments": CommentsSchema().dump(comments, many=True)}), 200


@comments_bp.route("/<int:blog_id>/add-comment", methods=['POST'])
@login_required
def add_blog_comment(blog_id):
    blog = db.session.query(Blogs).filter_by(id=blog_id).first()
    if blog is None:
        return jsonify({"response": "failure", "message": "blog doesn't exists"}), 404
    data = request.get_json()
    comment = db.session.query(Comments).filter_by(user_id=g.user_id, comment=data['comment']).first()
    if comment is not None:
        return jsonify({"response": "failure", "message": "Comment already exist by this user_id"}), 404
    try:
        comment = Comments(comment=data['comment'], user_id=g.user_id, blog_id=blog_id)
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        print("Exception occurred during saving comment", str(e))
        raise Exception("Exception occurred during saving comment")
    return jsonify({"response": "success", "message": "comment added successfully"}), 200


@comments_bp.route("/update-comment/<int:comment_id>", methods=['PATCH'])
@login_required
def update_blog_comment(comment_id):
    data = request.get_json()
    comment = db.session.query(Comments).filter_by(id=comment_id).first()
    if comment is None:
        return jsonify({"response": "failure", "message": "blog comment doesn't exist"}), 404

    try:
        if comment.user_id != g.user_id:
            return jsonify({"response": "failure", "message": "blog comment doesn't exist for given userId"}), 403
        if 'comment' in data:
            comment.comment = data['comment']
        comment.updated_at = datetime.utcnow()
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        print("Exception occurred during updating blog comment", str(e))
        raise Exception("Exception occurred during updating blog comment")
    return jsonify({"response": "success", "message": "comment updated successfully"}), 200


@comments_bp.route("/delete-comment/<int:comment_id>", methods=['DELETE'])
@login_required
def delete_blog_comment(comment_id):
    comment = db.session.query(Comments).filter_by(id=comment_id).first()
    if comment is None:
        return jsonify({"response": "failure", "message": "blog doesn't exist"}), 404
    if comment.user_id != g.user_id:
        return jsonify({"response": "failure", "message": "blog comment doesn't exist for given userId"}), 403
    try:
        db.session.delete(comment)
        db.session.commit()
    except Exception as e:
        print("Exception occurred during deleting blog comment", str(e))
        raise Exception("Exception occurred during deleting blog comment")
    return jsonify({"response": "success", "message": "Comment deleted successfully"}), 200
