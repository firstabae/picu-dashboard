"""
Supabase Storage utility for PICU Creator Dashboard
Handles file uploads to Supabase Storage
"""
import os
import uuid
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Check if supabase is available
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None
    logger.warning("Supabase package not installed. Using local storage.")


_supabase_client = None


def get_supabase_client() -> Client:
    """Get Supabase client instance (singleton)"""
    global _supabase_client
    
    if not SUPABASE_AVAILABLE:
        raise ImportError("Supabase package not installed. Run: pip install supabase")
    
    if _supabase_client is not None:
        return _supabase_client
    
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_KEY
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
    
    _supabase_client = create_client(url, key)
    return _supabase_client


def upload_design_image(file, creator_id: str) -> str:
    """
    Upload an image file to Supabase Storage
    
    Args:
        file: Django UploadedFile object
        creator_id: UUID of the creator for organizing files
    
    Returns:
        Public URL of the uploaded file
    """
    # Generate unique filename
    file_ext = os.path.splitext(file.name)[1].lower()
    if not file_ext:
        file_ext = '.png'  # Default extension
    unique_name = f"{uuid.uuid4()}{file_ext}"
    file_path = f"{creator_id}/{unique_name}"
    
    # Check if Supabase is configured
    supabase_url = getattr(settings, 'SUPABASE_URL', '')
    supabase_key = getattr(settings, 'SUPABASE_KEY', '')
    
    if not supabase_url or not supabase_key or not SUPABASE_AVAILABLE:
        logger.info("Supabase not configured, using local storage")
        return save_file_locally(file, f"designs/{file_path}")
    
    try:
        supabase = get_supabase_client()
        bucket = getattr(settings, 'SUPABASE_BUCKET', 'designs')
        
        # Read file content as bytes
        file.seek(0)  # Ensure we're at the beginning
        file_content = file.read()
        
        # Determine content type
        content_type = getattr(file, 'content_type', 'image/png')
        if not content_type:
            content_type = 'image/png'
        
        logger.info(f"Uploading to Supabase: bucket={bucket}, path={file_path}, size={len(file_content)} bytes")
        
        # Upload to Supabase Storage
        response = supabase.storage.from_(bucket).upload(
            path=file_path,
            file=file_content,
            file_options={
                "content-type": content_type,
                "upsert": "true"  # Overwrite if exists
            }
        )
        
        logger.info(f"Upload response: {response}")
        
        # Get public URL
        public_url = supabase.storage.from_(bucket).get_public_url(file_path)
        
        logger.info(f"Public URL: {public_url}")
        
        return public_url
        
    except Exception as e:
        logger.error(f"Supabase upload error: {type(e).__name__}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Fallback to local storage on error
        file.seek(0)  # Reset file pointer
        return save_file_locally(file, f"designs/{file_path}")


def save_file_locally(file, file_path: str) -> str:
    """
    Save file to local media directory (fallback when Supabase unavailable)
    
    Args:
        file: Django UploadedFile object
        file_path: Path within media directory
    
    Returns:
        URL path to the file
    """
    from django.core.files.storage import default_storage
    
    saved_path = default_storage.save(file_path, file)
    logger.info(f"Saved locally: /media/{saved_path}")
    return f"/media/{saved_path}"


def delete_design_image(file_url: str) -> bool:
    """
    Delete an image from Supabase Storage
    
    Args:
        file_url: URL of the file to delete
    
    Returns:
        True if deleted successfully, False otherwise
    """
    if not file_url:
        logger.warning("delete_design_image: No file URL provided")
        return False
    
    supabase_url = getattr(settings, 'SUPABASE_URL', '')
    
    if not supabase_url or not SUPABASE_AVAILABLE:
        logger.warning("delete_design_image: Supabase not configured")
        return False
    
    try:
        bucket = getattr(settings, 'SUPABASE_BUCKET', 'designs')
        
        # Extract file path from URL - handle different formats
        # Format 1: https://xxx.supabase.co/storage/v1/object/public/designs/path/file.png
        # Format 2: /storage/v1/object/public/designs/path/file.png
        
        file_path = None
        
        # Try to extract path from full Supabase URL
        storage_marker = f"/storage/v1/object/public/{bucket}/"
        if storage_marker in file_url:
            file_path = file_url.split(storage_marker)[-1]
        else:
            # Try alternative: just the bucket name in path
            bucket_marker = f"/{bucket}/"
            if bucket_marker in file_url:
                file_path = file_url.split(bucket_marker)[-1]
        
        if not file_path:
            logger.warning(f"delete_design_image: Could not extract path from URL: {file_url}")
            return False
        
        # Remove any query parameters
        if '?' in file_path:
            file_path = file_path.split('?')[0]
        
        logger.info(f"Attempting to delete from Supabase: bucket={bucket}, path={file_path}")
        
        supabase = get_supabase_client()
        response = supabase.storage.from_(bucket).remove([file_path])
        
        logger.info(f"Delete response: {response}")
        return True
        
    except Exception as e:
        logger.error(f"Supabase delete error: {type(e).__name__}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

