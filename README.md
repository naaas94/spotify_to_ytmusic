# Spotify to YouTube Music Migration Tool

A research project exploring automated playlist migration between music streaming platforms using reverse engineering techniques.

## Project Overview

This project investigates the feasibility of programmatically transferring music playlists from Spotify to YouTube Music without relying on official APIs. It serves as a technical exploration of web scraping, authentication mechanisms, and the challenges of working with closed platforms.

## What This Project Accomplishes

### ✅ Working Features

- **Spotify Data Export**: Complete backup of playlists, liked songs, and albums to local JSON files
- **YouTube Music Authentication**: Multiple authentication methods including OAuth and header-based auth
- **Song Search & Matching**: Three different algorithms for finding songs on YouTube Music
- **Playlist Management**: Create, list, and manage YouTube Music playlists
- **Command Line Interface**: Full CLI with multiple commands for different operations
- **Graphical Interface**: Basic GUI for user-friendly interaction
- **Batch Operations**: Transfer multiple playlists with configurable parameters

### 🔧 Technical Capabilities

- **Multiple Search Algorithms**: Exact, extended, and approximate matching
- **Error Recovery**: Retry mechanisms and graceful failure handling
- **Rate Limiting**: Configurable delays to respect platform limits
- **Dry Run Mode**: Test operations without making changes
- **Flexible Output**: Support for various data formats and encodings

## Technical Learnings & Challenges

### Authentication Complexity

**What We Learned**: YouTube Music's authentication system is highly dynamic and security-focused. The platform uses:
- Rapidly changing session tokens with heartbeat mechanisms
- Multi-layered header validation
- Frequent rotation of authentication parameters
- Anti-bot measures that detect automated access patterns

**Why This Matters**: This demonstrates how modern platforms protect against unauthorized access, making reverse engineering increasingly difficult and unreliable.

### API Stability Issues

**What We Learned**: The `ytmusicapi` library, while well-maintained, faces constant challenges:
- YouTube Music's internal API changes frequently
- Header requirements evolve with platform updates
- Success responses don't always indicate actual success
- Rate limiting is unpredictable and varies by account/region

**Technical Insight**: This highlights the fundamental challenge of relying on unofficial APIs - they're inherently fragile and require constant maintenance.

### Search Algorithm Effectiveness

**What We Learned**: Song matching across platforms is surprisingly complex:
- Metadata inconsistencies between platforms
- Regional availability differences
- Version variations (explicit vs clean, remixes, etc.)
- Artist name variations and aliases

**Positive Outcome**: The project successfully implemented multiple search strategies, achieving good match rates for well-known songs.

## Current Limitations

### Authentication Reliability

The most significant limitation is the authentication system's instability. While the project can successfully authenticate initially, the session tokens expire quickly (sometimes within minutes), making sustained operations unreliable.

### Success Detection

YouTube Music's API often returns success responses even when operations fail silently. This makes it difficult to verify whether songs were actually added to playlists.

### Scale Limitations

Due to the authentication and rate limiting challenges, the project is not suitable for large-scale migrations (thousands of songs) without significant manual intervention.

## Intended Use Cases

### What Works Well

1. **Small Playlist Migration**: Transferring playlists with 10-50 songs
2. **Research & Learning**: Understanding platform APIs and authentication
3. **Manual Verification**: Using the tool to find songs and manually verify matches
4. **Educational Purposes**: Learning about reverse engineering and web scraping

### Recommended Workflow

1. **Export Spotify Data**: Use the backup functionality to get your playlists
2. **Test Authentication**: Verify YTMusic connection works
3. **Small Batch Testing**: Start with a small playlist to test the process
4. **Manual Verification**: Check results and manually add missing songs
5. **Iterative Process**: Use the tool as a starting point, not a complete solution

## Installation & Setup

### Prerequisites

- Python 3.10+
- Spotify account with playlists
- YouTube Music account
- Firefox browser (for header extraction)

### Installation

```bash
git clone https://github.com/naaas94/spotify_to_ytmusic.git
cd spotify_to_ytmusic
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Authentication Setup

1. **YouTube Music Headers Method**:
   - Log into YouTube Music in Firefox
   - Open Developer Tools (F12) → Network tab
   - Filter by `/browse` and copy request headers
   - Save to `raw_headers.txt`
   - Run: `python spotify2ytmusic/ytmusic_credentials.py`

2. **OAuth Method** (Alternative):
   - Run: `ytmusicapi oauth`
   - Follow the browser authentication flow

### Spotify Data Export

```bash
python spotify2ytmusic/spotify_backup.py playlists.json --dump=liked,playlists --format=json
```

## Usage Examples

### Basic Operations

```bash
# List all playlists
python -m spotify2ytmusic list_playlists

# Transfer liked songs
python -m spotify2ytmusic load_liked

# Transfer specific playlist
python -m spotify2ytmusic copy_playlist <spotify_id> <ytmusic_id>

# Create new playlist
python -m spotify2ytmusic create_playlist "My New Playlist"
```

### Advanced Options

```bash
# Use approximate matching for difficult songs
python -m spotify2ytmusic copy_playlist <id> <id> --algo 2

# Test without making changes
python -m spotify2ytmusic copy_playlist <id> <id> --dry-run

# Adjust transfer speed
python -m spotify2ytmusic copy_playlist <id> <id> --track-sleep 0.5
```

## Potential Workarounds & Future Directions

### For Developers Interested in Continuing

1. **Header Rotation**: Implement automatic header refresh mechanisms
2. **Multiple Accounts**: Use multiple YTMusic accounts to distribute load
3. **Hybrid Approach**: Combine automated matching with manual verification
4. **Alternative Libraries**: Explore other YouTube Music libraries or direct API access
5. **Machine Learning**: Use ML to improve song matching accuracy

### For Users

1. **Manual Verification**: Always check results and manually add missing songs
2. **Small Batches**: Work with small playlists to minimize authentication issues
3. **Regular Re-authentication**: Re-run authentication setup when sessions expire
4. **Alternative Tools**: Consider paid services for large-scale migrations

## Project Structure

```
spotify_to_ytmusic/
├── spotify2ytmusic/
│   ├── backend.py          # Core migration logic
│   ├── cli.py              # Command line interface
│   ├── gui.py              # Graphical interface
│   ├── utils.py            # Utility functions
│   ├── ytmusic_credentials.py  # Authentication setup
│   └── spotify_backup.py   # Spotify data export
├── tests/                  # Test files
├── requirements.txt        # Dependencies
└── pyproject.toml         # Project configuration
```

## Contributing

This project is primarily for educational and research purposes. Contributions that focus on:
- Improving authentication reliability
- Enhancing search algorithms
- Adding better error detection
- Documenting technical findings

are welcome and valuable to the community.

## License

Creative Commons Zero v1.0 Universal - See LICENSE file for details.

## Acknowledgments

- The `ytmusicapi` library maintainers for their ongoing work
- The open-source community for reverse engineering insights
- All contributors who have shared their findings and experiences

---

**Note**: This project demonstrates the technical challenges of working with closed platforms and serves as a valuable learning resource for understanding modern web authentication and API reverse engineering techniques.
