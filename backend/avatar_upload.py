"""Avatar Upload Module for RPG Character Builder

This module handles character avatar image uploads, validation, processing,
and storage with support for multiple image formats.
"""

import os
import uuid
from PIL import Image
import hashlib

class AvatarUploader:
    def __init__(self, upload_dir='uploads/avatars', max_size_mb=5):
        self.upload_dir = upload_dir
        self.max_size_mb = max_size_mb
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.allowed_formats = ['PNG', 'JPEG', 'JPG', 'GIF', 'WEBP']
        self.thumbnail_size = (200, 200)
        
        # Create upload directory if it doesn't exist
        os.makedirs(upload_dir, exist_ok=True)
    
    def validate_image(self, file_path):
        """Validate uploaded image file"""
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > self.max_size_bytes:
            return False, f"File size exceeds {self.max_size_mb}MB limit"
        
        # Check image format
        try:
            with Image.open(file_path) as img:
                if img.format not in self.allowed_formats:
                    return False, f"Format {img.format} not allowed"
                
                # Check image dimensions
                if img.width > 2048 or img.height > 2048:
                    return False, "Image dimensions too large (max 2048x2048)"
                
                return True, "Valid image"
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"
    
    def generate_filename(self, original_filename):
        """Generate unique filename for uploaded avatar"""
        ext = os.path.splitext(original_filename)[1].lower()
        unique_id = str(uuid.uuid4())
        return f"avatar_{unique_id}{ext}"
    
    def create_thumbnail(self, image_path, output_path):
        """Create thumbnail version of avatar"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if needed
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Create thumbnail
                img.thumbnail(self.thumbnail_size, Image.Resampling.LANCZOS)
                img.save(output_path, 'JPEG', quality=85)
                return True, output_path
        except Exception as e:
            return False, f"Thumbnail creation failed: {str(e)}"
    
    def upload_avatar(self, file_path, character_id):
        """Upload and process avatar image"""
        # Validate image
        is_valid, message = self.validate_image(file_path)
        if not is_valid:
            return {'success': False, 'error': message}
        
        # Generate unique filename
        original_filename = os.path.basename(file_path)
        new_filename = self.generate_filename(original_filename)
        
        # Save paths
        avatar_path = os.path.join(self.upload_dir, new_filename)
        thumbnail_filename = f"thumb_{new_filename}"
        thumbnail_path = os.path.join(self.upload_dir, thumbnail_filename)
        
        try:
            # Copy/move original file
            with Image.open(file_path) as img:
                img.save(avatar_path)
            
            # Create thumbnail
            success, thumb_result = self.create_thumbnail(avatar_path, thumbnail_path)
            
            # Calculate file hash for deduplication
            with open(avatar_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            
            return {
                'success': True,
                'avatar_url': f"/avatars/{new_filename}",
                'thumbnail_url': f"/avatars/{thumbnail_filename}",
                'file_hash': file_hash,
                'character_id': character_id
            }
        except Exception as e:
            return {'success': False, 'error': f"Upload failed: {str(e)}"}
    
    def delete_avatar(self, avatar_url):
        """Delete avatar and thumbnail"""
        try:
            filename = os.path.basename(avatar_url)
            avatar_path = os.path.join(self.upload_dir, filename)
            thumbnail_path = os.path.join(self.upload_dir, f"thumb_{filename}")
            
            if os.path.exists(avatar_path):
                os.remove(avatar_path)
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            
            return {'success': True, 'message': 'Avatar deleted'}
        except Exception as e:
            return {'success': False, 'error': f"Delete failed: {str(e)}"}
