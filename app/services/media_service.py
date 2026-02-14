# app/services/media_service.py
import os
from werkzeug.utils import secure_filename
from app.utils.errors import FileSizeError, InvalidFileTypeError

class MediaService:
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    UPLOAD_FOLDER = '/storage/emulated/0/social-network/media'
    
    def save_media(self, file) -> str:
        """
        Save uploaded file and return URL.
        In production, this uploads to S3/CloudFront.
        """
        # Validate file
        if not self._allowed_file(file.filename):
            raise InvalidFileTypeError()
        
        # Check size (client can lie about Content-Length)
        file.seek(0, os.SEEK_END)
        size = file.tell()
        if size > self.MAX_FILE_SIZE:
            raise FileSizeError()
        file.seek(0)
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        filepath = os.path.join(self.UPLOAD_FOLDER, unique_filename)
        file.save(filepath)
        
        # Return URL (in production, return CDN URL)
        return f"/media/{unique_filename}"
