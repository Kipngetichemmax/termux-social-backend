# tests/unit/test_services/test_post_service.py
import pytest
from app.services.post_service import PostService
from app.utils.errors import ValidationError

class TestPostService:
    def test_create_post_success(self, db_session, sample_user):
        """Test successful post creation."""
        service = PostService()
        
        post = service.create_post(
            author_id=sample_user.id,
            content="Test post content"
        )
        
        assert post.id is not None
        assert post.content == "Test post content"
        assert post.author_id == sample_user.id
        assert post.like_count == 0
    
    def test_create_post_empty_content(self, sample_user):
        """Test validation: empty content should fail."""
        service = PostService()
        
        with pytest.raises(ValidationError):
            service.create_post(
                author_id=sample_user.id,
                content=""
            )
    
    def test_create_post_content_too_long(self, sample_user):
        """Test validation: content over 5000 chars should fail."""
        service = PostService()
        
        with pytest.raises(ValidationError):
            service.create_post(
                author_id=sample_user.id,
                content="a" * 5001
            )
