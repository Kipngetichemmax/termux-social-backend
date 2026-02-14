# app/services/feed_service.py
from app.repositories.post_repository import PostRepository
from app.repositories.follow_repository import FollowRepository
from typing import List, Dict
from app.utils.pagination import PaginationParams

class FeedService:
    def __init__(self):
        self.post_repo = PostRepository()
        self.follow_repo = FollowRepository()
    
    def get_user_feed(self, user_id: int, pagination: PaginationParams) -> Dict:
        """
        Generate feed for user: posts from followed users, reverse chronological.
        
        Engineering challenge: This is O(N*M) naive approach.
        - N = number of followed users
        - M = posts per user
        
        Optimization strategies:
        1. Denormalized feed table (fan-out on write)
        2. Materialized view of recent posts
        3. Cache layer (Redis sorted sets)
        
        For Termux: Query optimization + pagination is sufficient for <10k posts.
        """
        
        # Get list of users this user follows
        followed_user_ids = self.follow_repo.get_followed_user_ids(user_id)
        
        # Include user's own posts in feed (common pattern)
        followed_user_ids.append(user_id)
        
        # Fetch posts from followed users with pagination
        # This single query replaces N separate queries
        posts = self.post_repo.get_posts_by_authors(
            author_ids=followed_user_ids,
            pagination=pagination,
            include_deleted=False
        )
        
        # Hydrate with engagement data (likes, comments count already denormalized)
        # Check if current user liked each post
        post_ids = [post.id for post in posts]
        user_likes = self.post_repo.get_user_likes_for_posts(user_id, post_ids)
        
        feed_items = []
        for post in posts:
            feed_items.append({
                'id': post.id,
                'author': {
                    'id': post.author.id,
                    'username': post.author.username,
                    'profile_picture_url': post.author.profile_picture_url
                },
                'content': post.content,
                'media_url': post.media_url,
                'created_at': post.created_at.isoformat(),
                'like_count': post.like_count,
                'comment_count': post.comment_count,
                'liked_by_user': post.id in user_likes
            })
        
        return {
            'posts': feed_items,
            'pagination': pagination.to_dict()
        }
