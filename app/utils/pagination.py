# app/utils/pagination.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class PaginationParams:
    page: int = 1
    per_page: int = 20
    max_per_page: int = 100
    
    def __post_init__(self):
        # Enforce limits to prevent abuse
        self.per_page = min(self.per_page, self.max_per_page)
        self.page = max(1, self.page)
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page
    
    @property
    def limit(self) -> int:
        return self.per_page
    
    def to_dict(self) -> dict:
        return {
            'page': self.page,
            'per_page': self.per_page,
            'offset': self.offset
        }
    
    @classmethod
    def from_request(cls, request) -> 'PaginationParams':
        """Extract pagination from Flask request args."""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        return cls(page=page, per_page=per_page)
