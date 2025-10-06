# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-06

### Added
- 🔐 Initial authentication system with secure session persistence
- 📊 Account statistics viewing (followers, following, posts count)
- 👤 Current user information display (`whoami` command)
- 🔍 User profile lookup by username
- 🔎 User search functionality with customizable result limits
- 📱 Instagram feed browsing from terminal
- 📸 Photo posting capability with caption support
- 🎨 Beautiful terminal UI using Rich library with colors, tables, and emojis
- ⚡ Rate limiting handling with automatic retry and exponential backoff
- 🔒 Secure session file storage with proper permissions (600)
- 📝 Comprehensive CLI help documentation for all commands
- ⚙️ Environment configuration support via .env files
- 🛠️ Modular architecture with separate auth, client, and utils modules

### Features by Command
- `login` - Authenticate with Instagram credentials
- `logout` - Remove saved session
- `stats` - View your account statistics
- `whoami` - Display current user information
- `user <username>` - Look up any user's profile
- `search <query>` - Search for users by name or username
- `feed` - Browse your Instagram feed
- `post <photo>` - Upload and post photos with captions

[0.1.0]: https://github.com/yourusername/instagram-cli/releases/tag/v0.1.0
