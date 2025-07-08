# Spotify to YouTube Music Migration Tool

A fast, optimized tool for migrating your Spotify playlists and liked songs to YouTube Music.

## ✨ Features

- **Fast Migration**: Optimized algorithms for quick playlist transfers
- **Smart Song Matching**: Multiple search algorithms for accurate song matching
- **Batch Operations**: Transfer multiple playlists at once
- **GUI Interface**: User-friendly graphical interface
- **Command Line**: Full CLI support for automation
- **Error Recovery**: Robust retry mechanisms and error handling
- **Dry Run Mode**: Test transfers without making changes

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/linsomniac/spotify_to_ytmusic.git
cd spotify_to_ytmusic
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 2. Setup YouTube Music Authentication

1. Log into YouTube Music in Firefox
2. Open Developer Tools (F12) → Network tab
3. Filter by `/browse` and copy request headers
4. Paste into `raw_headers.txt`
5. Run: `python spotify2ytmusic/ytmusic_credentials.py`

### 3. Backup Spotify Data

```bash
python spotify2ytmusic/spotify_backup.py playlists.json --dump=liked,playlists --format=json
```

### 4. Start Migration

**GUI Mode:**
```bash
python -m spotify2ytmusic gui
```

**Command Line:**
```bash
# Transfer liked songs
python -m spotify2ytmusic load_liked

# Transfer all playlists
python -m spotify2ytmusic copy_all_playlists

# Transfer specific playlist
python -m spotify2ytmusic copy_playlist <spotify_id> <ytmusic_id>
```

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `list_playlists` | Show Spotify and YTMusic playlists |
| `load_liked` | Transfer Spotify liked songs to YTMusic |
| `load_liked_albums` | Transfer Spotify liked albums |
| `copy_playlist` | Transfer specific playlist |
| `copy_all_playlists` | Transfer all playlists |
| `create_playlist` | Create new YTMusic playlist |
| `search` | Search for songs on YTMusic |
| `gui` | Launch graphical interface |

## 🔧 Advanced Usage

### Batch Transfer Multiple Playlists

```python
from spotify2ytmusic import utils

playlists = ["Chill", "Lounge", "Workout"]
results = utils.batch_transfer_playlists(playlists, track_sleep=0.5)
```

### Check Connection Status

```python
from spotify2ytmusic import utils

if utils.check_ytmusic_connection():
    print("✅ YTMusic connection successful")
```

### Search Algorithms

The tool supports 3 search algorithms:

- **Algorithm 0** (Default): Exact matching - fastest, most accurate
- **Algorithm 1**: Extended matching - searches for exact title/artist/album match
- **Algorithm 2**: Approximate matching - fuzzy matching for difficult songs

```bash
python -m spotify2ytmusic copy_playlist <id> <id> --algo 2
```

### Performance Options

```bash
# Faster transfer (less sleep between tracks)
python -m spotify2ytmusic copy_playlist <id> <id> --track-sleep 0.05

# Test run without making changes
python -m spotify2ytmusic copy_playlist <id> <id> --dry-run

# Don't reverse playlist order
python -m spotify2ytmusic copy_playlist <id> <id> --no-reverse-playlist
```

## 🛠️ Utility Functions

The optimized codebase includes utility functions for common tasks:

```python
from spotify2ytmusic import utils

# List all Spotify playlists
utils.list_spotify_playlists()

# Convert library format
utils.convert_spotify_library_to_playlists()

# Transfer by playlist ID
utils.transfer_playlist_by_id("spotify_id", "ytmusic_id")
```

## 📊 Performance Optimizations

### What's Been Optimized

1. **Code Structure**: Eliminated duplicate code and improved modularity
2. **Error Handling**: Better exception handling and recovery
3. **Type Safety**: Added proper type hints throughout
4. **Memory Usage**: Optimized data structures and iterators
5. **Speed**: Reduced unnecessary API calls and improved caching
6. **Cohesion**: Better separation of concerns and responsibilities

### Performance Tips

- Use `--track-sleep 0.05` for faster transfers (if your connection can handle it)
- Use `--algo 0` for fastest matching (works for 95% of songs)
- Use `--dry-run` to test before actual transfer
- Transfer large playlists during off-peak hours

## 🔍 Troubleshooting

### Common Issues

**"No file 'oauth.json' exists"**
- Run the YouTube Music authentication setup again

**"Could not find Spotify playlist"**
- Ensure `playlists.json` exists and contains your playlists
- Re-run the Spotify backup process

**"Unable to look up song on YTMusic"**
- Try using `--algo 2` for approximate matching
- Some songs may not be available on YouTube Music

**Rate limiting errors**
- Increase `--track-sleep` value (try 1.0 or higher)
- Wait a few minutes and retry

### Debug Mode

Enable verbose output to see detailed information:

```bash
python -m spotify2ytmusic copy_playlist <id> <id> --track-sleep 1.0
```

## 📁 Project Structure

```
spotify_to_ytmusic/
├── spotify2ytmusic/
│   ├── backend.py      # Core migration logic (optimized)
│   ├── cli.py          # Command line interface (optimized)
│   ├── gui.py          # Graphical interface
│   ├── utils.py        # Utility functions (new)
│   └── __main__.py     # Entry point
├── playlists.json      # Your Spotify data
├── oauth.json          # YTMusic credentials
├── requirements.txt    # Dependencies
└── example_usage.py    # Usage examples
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

Creative Commons Zero v1.0 Universal

## 🙏 Acknowledgments

- Original work by Sean Reifschneider
- GUI implementation by Yoween
- Optimizations and improvements by the community 