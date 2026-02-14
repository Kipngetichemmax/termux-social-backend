from flask import Blueprint, jsonify, request
from app.services.post_service import PostService

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/', methods=['GET'])
def get_posts():
    posts = PostService.list_posts()
    return jsonify(posts), 200

@posts_bp.route('/', methods=['POST'])
def create_post():
    # Note: In a real app, user_id would come from the JWT token
    data = request.get_json()
    post = PostService.create_post(data, user_id=1) 
    return jsonify({"message": "Post created", "id": post.id}), 201

