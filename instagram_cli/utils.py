"""Utility functions for Instagram CLI."""

import os
from pathlib import Path
from functools import wraps
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import click

console = Console()


def get_session_file_path() -> Path:
    """Get the path to the Instagram session file."""
    session_file = os.getenv("INSTAGRAM_SESSION_FILE", "~/.instagram_session.json")
    return Path(session_file).expanduser()


def get_config_dir() -> Path:
    """Get the configuration directory for Instagram CLI."""
    config_dir = Path.home() / ".config" / "instagram-cli"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def requires_auth(func):
    """Decorator to ensure user is authenticated before running command."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        from instagram_cli.auth import SessionManager
        
        session_manager = SessionManager()
        if not session_manager.is_authenticated():
            console.print("[red]❌ Not authenticated. Please run 'instagram-cli login' first.[/red]")
            raise click.Abort()
        return func(*args, **kwargs)
    return wrapper


def format_user_info(user_data: dict) -> Panel:
    """Format user information as a rich panel."""
    info_text = f"""
[bold cyan]Username:[/bold cyan] @{user_data.get('username', 'N/A')}
[bold cyan]Full Name:[/bold cyan] {user_data.get('full_name', 'N/A')}
[bold cyan]Biography:[/bold cyan] {user_data.get('biography', 'N/A')}
[bold cyan]Followers:[/bold cyan] {user_data.get('follower_count', 0):,}
[bold cyan]Following:[/bold cyan] {user_data.get('following_count', 0):,}
[bold cyan]Posts:[/bold cyan] {user_data.get('media_count', 0):,}
[bold cyan]Is Private:[/bold cyan] {'Yes' if user_data.get('is_private', False) else 'No'}
[bold cyan]Is Verified:[/bold cyan] {'Yes ✓' if user_data.get('is_verified', False) else 'No'}
    """.strip()
    
    return Panel(info_text, title=f"👤 User Profile", border_style="cyan", box=box.ROUNDED)


def format_account_stats(stats: dict) -> Panel:
    """Format account statistics as a rich panel."""
    stats_text = f"""
[bold green]Followers:[/bold green] {stats.get('followers', 0):,}
[bold green]Following:[/bold green] {stats.get('following', 0):,}
[bold green]Posts:[/bold green] {stats.get('posts', 0):,}
    """.strip()
    
    return Panel(stats_text, title="📊 Account Statistics", border_style="green", box=box.ROUNDED)


def format_search_results(users: list) -> Table:
    """Format user search results as a rich table."""
    table = Table(title="🔍 Search Results", box=box.ROUNDED, border_style="blue")
    
    table.add_column("Username", style="cyan", no_wrap=True)
    table.add_column("Full Name", style="white")
    table.add_column("Followers", style="green", justify="right")
    table.add_column("Verified", style="yellow", justify="center")
    
    for user in users:
        table.add_row(
            f"@{user.get('username', 'N/A')}",
            user.get('full_name', 'N/A'),
            f"{user.get('follower_count', 0):,}",
            "✓" if user.get('is_verified', False) else ""
        )
    
    return table


def format_feed_posts(posts: list) -> Table:
    """Format feed posts as a rich table."""
    table = Table(title="📱 Feed Posts", box=box.ROUNDED, border_style="magenta")
    
    table.add_column("#", style="dim", width=4)
    table.add_column("Username", style="cyan", no_wrap=True)
    table.add_column("Caption", style="white")
    table.add_column("Likes", style="red", justify="right")
    table.add_column("Comments", style="blue", justify="right")
    
    for idx, post in enumerate(posts, 1):
        caption = post.get('caption', {}).get('text', 'No caption') if post.get('caption') else 'No caption'
        # Truncate long captions
        if len(caption) > 50:
            caption = caption[:47] + "..."
        
        table.add_row(
            str(idx),
            f"@{post.get('user', {}).get('username', 'N/A')}",
            caption,
            f"{post.get('like_count', 0):,}",
            f"{post.get('comment_count', 0):,}"
        )
    
    return table


def success_message(message: str):
    """Display a success message."""
    console.print(f"[green]✅ {message}[/green]")


def error_message(message: str):
    """Display an error message."""
    console.print(f"[red]❌ {message}[/red]")


def info_message(message: str):
    """Display an info message."""
    console.print(f"[blue]ℹ️  {message}[/blue]")


def warning_message(message: str):
    """Display a warning message."""
    console.print(f"[yellow]⚠️  {message}[/yellow]")
