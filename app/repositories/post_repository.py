from app.extensions import db
from app.models import Post

class PostRepository:
    @staticmethod
    def get_all():
        return Post.query.order_by(Post.timestamp.desc()).all()

    @staticmethod
    def get_by_id(post_id):
        return Post.query.get(post_id)

    @staticmethod
    def create(body, user_id):
        post = Post(body=body, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return post

