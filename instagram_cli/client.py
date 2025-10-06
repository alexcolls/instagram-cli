"""Instagram API client wrapper."""

from pathlib import Path
from typing import List, Dict, Optional
import time

from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    ClientError,
    RateLimitError
)

from instagram_cli.auth import SessionManager
from instagram_cli.utils import error_message, info_message, success_message


class InstaClient:
    """Wrapper around instagrapi Client with additional functionality."""
    
    def __init__(self):
        """Initialize the Instagram client."""
        self.session_manager = SessionManager()
        self._client: Optional[Client] = None
    
    @property
    def client(self) -> Client:
        """Get or create an authenticated client."""
        if self._client is None:
            self._client = self.session_manager.get_client()
        return self._client
    
    def _retry_on_rate_limit(self, func, *args, **kwargs):
        """Execute a function with retry logic for rate limiting."""
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except RateLimitError:
                if attempt < max_retries - 1:
                    info_message(f"Rate limited. Waiting {retry_delay} seconds before retry...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    error_message("Rate limit exceeded. Please try again later.")
                    raise
            except Exception as e:
                raise
    
    def get_account_stats(self) -> Dict[str, int]:
        """
        Get statistics for the authenticated account.
        
        Returns:
            Dictionary with followers, following, and posts counts
        """
        try:
            user_id = self.client.user_id
            user_info = self.client.user_info(user_id)
            
            return {
                'followers': user_info.follower_count,
                'following': user_info.following_count,
                'posts': user_info.media_count
            }
        except LoginRequired:
            error_message("Session expired. Please login again.")
            raise
        except Exception as e:
            error_message(f"Failed to get account stats: {str(e)}")
            raise
    
    def get_user_info(self, username: str) -> Dict:
        """
        Get information about a user.
        
        Args:
            username: Instagram username (without @)
            
        Returns:
            Dictionary with user information
        """
        try:
            # Remove @ if present
            username = username.lstrip('@')
            
            user_id = self._retry_on_rate_limit(self.client.user_id_from_username, username)
            user_info = self._retry_on_rate_limit(self.client.user_info, user_id)
            
            return {
                'username': user_info.username,
                'full_name': user_info.full_name,
                'biography': user_info.biography,
                'follower_count': user_info.follower_count,
                'following_count': user_info.following_count,
                'media_count': user_info.media_count,
                'is_private': user_info.is_private,
                'is_verified': user_info.is_verified,
                'external_url': user_info.external_url,
                'profile_pic_url': user_info.profile_pic_url
            }
        except Exception as e:
            error_message(f"Failed to get user info for @{username}: {str(e)}")
            raise
    
    def search_users(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for users by username or name.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of user dictionaries
        """
        try:
            users = self._retry_on_rate_limit(self.client.search_users, query)
            
            results = []
            for user in users[:limit]:
                results.append({
                    'username': user.username,
                    'full_name': user.full_name,
                    'follower_count': user.follower_count,
                    'is_verified': user.is_verified,
                    'is_private': user.is_private
                })
            
            return results
        except Exception as e:
            error_message(f"Failed to search users: {str(e)}")
            raise
    
    def get_feed(self, limit: int = 20) -> List[Dict]:
        """
        Get posts from the user's feed.
        
        Args:
            limit: Maximum number of posts to retrieve
            
        Returns:
            List of post dictionaries
        """
        try:
            feed = self._retry_on_rate_limit(self.client.get_timeline_feed)
            
            posts = []
            for media in feed.get('feed_items', [])[:limit]:
                if 'media_or_ad' in media:
                    post = media['media_or_ad']
                    posts.append({
                        'id': post.get('id'),
                        'user': {
                            'username': post.get('user', {}).get('username'),
                            'full_name': post.get('user', {}).get('full_name')
                        },
                        'caption': post.get('caption'),
                        'like_count': post.get('like_count', 0),
                        'comment_count': post.get('comment_count', 0),
                        'media_type': post.get('media_type'),
                        'taken_at': post.get('taken_at')
                    })
            
            return posts
        except Exception as e:
            error_message(f"Failed to get feed: {str(e)}")
            raise
    
    def post_photo(self, photo_path: str, caption: str = "") -> bool:
        """
        Post a photo to Instagram.
        
        Args:
            photo_path: Path to the photo file
            caption: Caption for the photo
            
        Returns:
            True if successful
        """
        try:
            photo_file = Path(photo_path).expanduser()
            
            if not photo_file.exists():
                error_message(f"Photo file not found: {photo_path}")
                return False
            
            if not photo_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                error_message("Photo must be JPG, JPEG, or PNG format")
                return False
            
            info_message(f"Uploading photo: {photo_file.name}")
            
            media = self._retry_on_rate_limit(
                self.client.photo_upload,
                photo_file,
                caption
            )
            
            if media:
                success_message(f"Photo posted successfully! Media ID: {media.pk}")
                return True
            else:
                error_message("Failed to post photo")
                return False
                
        except Exception as e:
            error_message(f"Failed to post photo: {str(e)}")
            raise
    
    def get_current_user(self) -> Dict:
        """
        Get information about the currently authenticated user.
        
        Returns:
            Dictionary with current user information
        """
        try:
            user_id = self.client.user_id
            user_info = self.client.user_info(user_id)
            
            return {
                'username': user_info.username,
                'full_name': user_info.full_name,
                'biography': user_info.biography,
                'follower_count': user_info.follower_count,
                'following_count': user_info.following_count,
                'media_count': user_info.media_count,
                'is_private': user_info.is_private,
                'is_verified': user_info.is_verified,
                'user_id': str(user_id)
            }
        except Exception as e:
            error_message(f"Failed to get current user info: {str(e)}")
            raise
