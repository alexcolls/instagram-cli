"""Command-line interface for Instagram CLI."""

import click
from pathlib import Path

from instagram_cli.auth import SessionManager
from instagram_cli.client import InstaClient
from instagram_cli.utils import (
    console,
    requires_auth,
    format_user_info,
    format_account_stats,
    format_search_results,
    format_feed_posts,
    success_message,
    error_message,
    info_message
)


@click.group()
@click.version_option(version="0.1.0", prog_name="instagram-cli")
def main():
    """
    📸 Instagram CLI - Easy-to-use Instagram CLI for managing accounts and stats.
    
    Authenticate, view stats, post photos, and more from your terminal!
    """
    pass


@main.command()
@click.option('--username', '-u', prompt='Instagram username', help='Your Instagram username')
@click.option('--password', '-p', prompt='Password', hide_input=True, help='Your Instagram password')
def login(username: str, password: str):
    """
    🔐 Login to Instagram.
    
    Authenticate with your Instagram credentials. Session will be saved securely.
    """
    try:
        session_manager = SessionManager()
        session_manager.login(username, password)
    except KeyboardInterrupt:
        info_message("\nLogin cancelled")
    except Exception as e:
        error_message(f"Login failed: {str(e)}")
        raise click.Abort()


@main.command()
def logout():
    """
    🚪 Logout from Instagram.
    
    Remove saved session and logout from Instagram.
    """
    try:
        session_manager = SessionManager()
        session_manager.logout()
    except Exception as e:
        error_message(f"Logout failed: {str(e)}")
        raise click.Abort()


@main.command()
@requires_auth
def stats():
    """
    📊 View your account statistics.
    
    Display followers, following, and posts count for your account.
    """
    try:
        client = InstaClient()
        account_stats = client.get_account_stats()
        
        panel = format_account_stats(account_stats)
        console.print(panel)
        
    except Exception as e:
        error_message(f"Failed to get stats: {str(e)}")
        raise click.Abort()


@main.command()
@requires_auth
def whoami():
    """
    👤 Display current user information.
    
    Show detailed information about the currently authenticated user.
    """
    try:
        client = InstaClient()
        user_info = client.get_current_user()
        
        panel = format_user_info(user_info)
        console.print(panel)
        
    except Exception as e:
        error_message(f"Failed to get user info: {str(e)}")
        raise click.Abort()


@main.command()
@click.argument('username')
@requires_auth
def user(username: str):
    """
    🔍 View user profile information.
    
    Display detailed information about any Instagram user.
    
    USERNAME: Instagram username to lookup (with or without @)
    """
    try:
        client = InstaClient()
        user_info = client.get_user_info(username)
        
        panel = format_user_info(user_info)
        console.print(panel)
        
    except Exception as e:
        error_message(f"Failed to get user info: {str(e)}")
        raise click.Abort()


@main.command()
@click.argument('query')
@click.option('--limit', '-l', default=10, help='Maximum number of results to show')
@requires_auth
def search(query: str, limit: int):
    """
    🔎 Search for Instagram users.
    
    Search for users by username or name.
    
    QUERY: Search term (username or name)
    """
    try:
        client = InstaClient()
        results = client.search_users(query, limit)
        
        if not results:
            info_message(f"No users found for query: {query}")
            return
        
        table = format_search_results(results)
        console.print(table)
        console.print(f"\n[dim]Found {len(results)} user(s)[/dim]")
        
    except Exception as e:
        error_message(f"Search failed: {str(e)}")
        raise click.Abort()


@main.command()
@click.option('--limit', '-l', default=20, help='Number of posts to retrieve')
@requires_auth
def feed(limit: int):
    """
    📱 View your Instagram feed.
    
    Display recent posts from accounts you follow.
    """
    try:
        client = InstaClient()
        info_message(f"Fetching {limit} posts from your feed...")
        
        posts = client.get_feed(limit)
        
        if not posts:
            info_message("No posts found in your feed")
            return
        
        table = format_feed_posts(posts)
        console.print(table)
        console.print(f"\n[dim]Showing {len(posts)} post(s)[/dim]")
        
    except Exception as e:
        error_message(f"Failed to get feed: {str(e)}")
        raise click.Abort()


@main.command()
@click.argument('photo', type=click.Path(exists=True))
@click.option('--caption', '-c', default='', help='Caption for the photo')
@requires_auth
def post(photo: str, caption: str):
    """
    📸 Post a photo to Instagram.
    
    Upload and post a photo with an optional caption.
    
    PHOTO: Path to the photo file (JPG, JPEG, or PNG)
    """
    try:
        client = InstaClient()
        
        photo_path = Path(photo).resolve()
        
        if client.post_photo(str(photo_path), caption):
            success_message("Photo posted successfully!")
        else:
            error_message("Failed to post photo")
            raise click.Abort()
            
    except Exception as e:
        error_message(f"Failed to post photo: {str(e)}")
        raise click.Abort()


if __name__ == '__main__':
    main()
