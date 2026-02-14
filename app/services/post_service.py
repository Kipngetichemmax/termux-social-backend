from app.repositories.post_repository import PostRepository
from app.utils.errors import APIError

class PostService:
    @staticmethod
    def list_posts():
        posts = PostRepository.get_all()
        return [{"id": p.id, "body": p.body, "author_id": p.user_id} for p in posts]

    @staticmethod
    def create_post(data, user_id):
        body = data.get('body')
        if not body:
            raise APIError("Post body is required", status_code=400)
        
        return PostRepository.create(body, user_id)

