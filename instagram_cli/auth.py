"""Authentication and session management for Instagram CLI."""

import os
import json
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    BadPassword,
    ChallengeRequired,
    TwoFactorRequired
)

from instagram_cli.utils import get_session_file_path, success_message, error_message, info_message


class SessionManager:
    """Manages Instagram authentication sessions."""
    
    def __init__(self):
        """Initialize the session manager."""
        load_dotenv()
        self.session_file = get_session_file_path()
        self.client: Optional[Client] = None
    
    def is_authenticated(self) -> bool:
        """Check if there's an active authenticated session."""
        if not self.session_file.exists():
            return False
        
        try:
            client = Client()
            client.load_settings(self.session_file)
            # Try to get user info to verify session is still valid
            client.account_info()
            return True
        except Exception:
            return False
    
    def login(self, username: str, password: str) -> Client:
        """
        Login to Instagram with username and password.
        
        Args:
            username: Instagram username
            password: Instagram password
            
        Returns:
            Authenticated Client instance
            
        Raises:
            Various instagrapi exceptions on authentication failure
        """
        client = Client()
        
        # Try to load existing session first
        if self.session_file.exists():
            try:
                client.load_settings(self.session_file)
                info_message("Found existing session, attempting to reuse...")
                client.login(username, password)
                success_message(f"Logged in as @{username} using existing session")
                self.client = client
                return client
            except Exception as e:
                info_message(f"Existing session invalid, creating new one...")
        
        # Create new session
        try:
            info_message("Logging in to Instagram...")
            client.login(username, password)
            
            # Save session
            self._save_session(client)
            success_message(f"Successfully logged in as @{username}")
            self.client = client
            return client
            
        except BadPassword:
            error_message("Invalid password. Please check your credentials.")
            raise
        except TwoFactorRequired:
            error_message("Two-factor authentication is required. Please disable 2FA or use app-specific password.")
            raise
        except ChallengeRequired as e:
            error_message("Instagram requires additional verification. Please verify your account through the app first.")
            raise
        except Exception as e:
            error_message(f"Login failed: {str(e)}")
            raise
    
    def _save_session(self, client: Client):
        """Save the client session to file."""
        try:
            # Ensure parent directory exists
            self.session_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Save settings
            client.dump_settings(self.session_file)
            
            # Set secure permissions (readable/writable only by user)
            self.session_file.chmod(0o600)
            
            info_message(f"Session saved to {self.session_file}")
        except Exception as e:
            error_message(f"Failed to save session: {str(e)}")
    
    def logout(self):
        """Logout and remove saved session."""
        try:
            if self.session_file.exists():
                self.session_file.unlink()
                success_message("Logged out successfully")
            else:
                info_message("No active session found")
        except Exception as e:
            error_message(f"Failed to logout: {str(e)}")
            raise
    
    def get_client(self) -> Client:
        """
        Get an authenticated client instance.
        
        Returns:
            Authenticated Client instance
            
        Raises:
            LoginRequired if not authenticated
        """
        if not self.is_authenticated():
            raise LoginRequired("Not authenticated. Please login first.")
        
        client = Client()
        client.load_settings(self.session_file)
        
        # Re-login to ensure session is valid
        try:
            client.get_timeline_feed()
        except LoginRequired:
            error_message("Session expired. Please login again.")
            raise
        
        return client
    
    def get_current_username(self) -> Optional[str]:
        """Get the username of the currently authenticated user."""
        try:
            client = self.get_client()
            user_id = client.user_id
            user_info = client.user_info(user_id)
            return user_info.username
        except Exception:
            return None
