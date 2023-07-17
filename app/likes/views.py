from flask import g, jsonify
from app import db
from app.likes import bloglikes_bp
from app.likes.models import BlogLikes
from lib.jwt_utils import login_required


@bloglikes_bp.route("/like/<int:blog_id>", methods=['GET'])
@login_required
def like_blog(blog_id):
    blog_like = db.session.query(BlogLikes).filter(BlogLikes.user_id == g.user_id, BlogLikes.blog_id == blog_id).first()
    if blog_like is not None:
        return jsonify({"response": "failure", "message": "blog was already liked by you"}), 403

    blog_like = BlogLikes(user_id=g.user_id, blog_id=blog_id, status=True)
    db.session.add(blog_like)
    db.session.commit()
    return jsonify({"response": "success", "message": "Blog like successfully"}), 200


@bloglikes_bp.route("/dislike/<int:blog_id>", methods=['GET'])
@login_required
def dislike_blog(blog_id):
    blog_like = db.session.query(BlogLikes).filter(BlogLikes.user_id == g.user_id, BlogLikes.blog_id == blog_id).first()
    if blog_like is None:
        return jsonify({"response": "failure", "message": "you have not liked this blog yet"}), 404

    db.session.delete(blog_like)
    db.session.commit()
    return jsonify({"response": "success", "message": "Blog disliked successfully"}), 200


@bloglikes_bp.route("/count/<int:blog_id>", methods=['GET'])
def likes_count(blog_id):
    blogs_count = db.session.query(BlogLikes).filter_by(blog_id=blog_id).count()
    return jsonify({"response": "success", "count": blogs_count}), 200
