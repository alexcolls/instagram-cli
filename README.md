# 📸 Instagram CLI

Easy-to-use Instagram CLI for creating and managing accounts and stats from your terminal.

## ✨ Features

- 🔐 **Authentication**: Secure login with session persistence
- 📊 **Account Stats**: View followers, following, and posts count
- 👤 **User Profiles**: Get detailed information about any Instagram user
- 🔎 **User Search**: Search for users by username or name
- 📱 **Feed Viewer**: Browse your Instagram feed from the terminal
- 📸 **Photo Posting**: Upload and post photos with captions
- 🎨 **Beautiful UI**: Rich formatting with colors, tables, and emojis

## 📋 Requirements

- Python 3.9 or higher
- Poetry (for dependency management)
- An Instagram account

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/instagram-cli.git
   cd instagram-cli
   ```

2. **Install dependencies with Poetry**:
   ```bash
   poetry install
   ```

3. **Activate the virtual environment**:
   ```bash
   poetry shell
   ```

4. **Optional: Configure environment** (usually not needed):
   ```bash
   cp .env.sample .env
   # Edit .env if you want to customize the session file location
   ```

## 📖 Usage

### Login

Authenticate with your Instagram credentials:

```bash
instagram-cli login
```

You'll be prompted for your username and password. The session will be saved securely.

### View Your Account Stats

Display your followers, following, and posts count:

```bash
instagram-cli stats
```

### View Current User Info

Show detailed information about your authenticated account:

```bash
instagram-cli whoami
```

### Look Up a User Profile

Get detailed information about any Instagram user:

```bash
instagram-cli user instagram
instagram-cli user @natgeo
```

### Search for Users

Search for users by username or name:

```bash
instagram-cli search "john smith"
instagram-cli search --limit 20 photographer
```

### View Your Feed

Browse posts from accounts you follow:

```bash
instagram-cli feed
instagram-cli feed --limit 30
```

### Post a Photo

Upload and post a photo with an optional caption:

```bash
instagram-cli post /path/to/photo.jpg
instagram-cli post /path/to/photo.jpg --caption "Beautiful sunset! 🌅"
```

### Logout

Remove saved session and logout:

```bash
instagram-cli logout
```

### Get Help

View available commands and options:

```bash
instagram-cli --help
instagram-cli <command> --help
```

## 🎨 Command Reference

| Command | Description | Example |
|---------|-------------|----------|
| `login` | Authenticate with Instagram | `instagram-cli login` |
| `logout` | Remove session and logout | `instagram-cli logout` |
| `stats` | View your account statistics | `instagram-cli stats` |
| `whoami` | Show current user information | `instagram-cli whoami` |
| `user <username>` | View any user's profile | `instagram-cli user nasa` |
| `search <query>` | Search for users | `instagram-cli search "travel"` |
| `feed` | View your Instagram feed | `instagram-cli feed --limit 30` |
| `post <photo>` | Post a photo | `instagram-cli post pic.jpg -c "Hi!"` |

## ⚙️ Configuration

The CLI stores the session in `~/.instagram_session.json` by default. You can customize this by:

1. Creating a `.env` file (copy from `.env.sample`)
2. Setting the `INSTAGRAM_SESSION_FILE` variable to your preferred path

## 🔒 Security Notes

- Your password is never stored - only the session token
- Session files are created with secure permissions (600)
- Use app-specific passwords if you have 2FA enabled
- Never commit your `.env` file or session files to version control

## 🐛 Troubleshooting

### "Challenge Required" Error

If Instagram requires additional verification:
1. Login through the Instagram app or website
2. Complete any security challenges
3. Try logging in again through the CLI

### "Rate Limit" Error

Instagram limits API requests. If you hit the limit:
- Wait a few minutes before retrying
- Reduce the `--limit` parameter for feed and search commands
- The CLI automatically retries with exponential backoff

### Two-Factor Authentication (2FA)

If you have 2FA enabled:
- Disable 2FA temporarily, or
- Generate an app-specific password from Instagram settings

### Session Expired

If your session expires:
```bash
instagram-cli logout
instagram-cli login
```

## 🛠️ Development

### Running Tests

```bash
poetry run pytest
```

### Code Formatting

```bash
poetry run black instagram_cli/
poetry run isort instagram_cli/
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

This tool uses the unofficial Instagram API. Use at your own risk. Instagram may change their API at any time, which could break functionality. Be respectful of Instagram's terms of service and rate limits.

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

Made with ❤️ by Alex Colls Outumuro
