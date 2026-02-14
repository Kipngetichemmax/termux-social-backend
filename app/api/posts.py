from flask import Blueprint, jsonify, request
from app.services.post_service import PostService
from app.utils.auth import jwt_required
from app.models import User

posts_bp = Blueprint("posts_bp", __name__)

# -----------------------
# List all posts (public feed)
# -----------------------
@posts_bp.route("/", methods=["GET"])
def get_posts():
    posts = PostService.list_posts()  # Returns list of posts
    feed = []
    for post in posts:
        feed.append({
            "id": post.id,
            "content": post.content,
            "user": {
                "id": post.user.id,
                "username": post.user.username
            },
            "timestamp": post.timestamp.isoformat()
        })
    return jsonify(feed), 200


# -----------------------
# Create a post (protected)
# -----------------------
@posts_bp.route("/create", methods=["POST"])
@jwt_required
def create_post():
    data = request.get_json()
    content = data.get("content")
    if not content:
        return jsonify({"error": "Post content required"}), 400

    # Use user_id from JWT token
    post = PostService.create_post(data, user_id=request.user_id)
    return jsonify({
        "message": "Post created",
        "post": {
            "id": post.id,
            "content": post.content,
            "user_id": post.user_id
        }
    }), 201


# -----------------------
# Optional: Feed for logged-in users (reverse chronological)
# -----------------------
@posts_bp.route("/feed", methods=["GET"])
@jwt_required
def feed():
    posts = PostService.list_posts(order_by="desc")  # New param in service
    feed_list = []
    for post in posts:
        feed_list.append({
            "id": post.id,
            "content": post.content,
            "user": {
                "id": post.user.id,
                "username": post.user.username
            },
            "timestamp": post.timestamp.isoformat()
        })
    return jsonify(feed_list), 200
