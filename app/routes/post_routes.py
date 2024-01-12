from flask import Blueprint, jsonify, request
from app.models.post import BlogPost

post_bp = Blueprint('post', __name__)

@post_bp.route('/posts', methods=['GET'])
def get_all_posts():
    # posts = BlogPost.get_all_posts()
    posts = ["first", "second", "third", "fourth"]
    return jsonify(posts=posts)

@post_bp.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    BlogPost.create_post(title, content)

    return jsonify(message="Post created successfully!")
