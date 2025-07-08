#!/usr/bin/env python3

"""
Example usage of the Spotify to YouTube Music migration research project.

This demonstrates the capabilities and limitations of the tool.
Note: This is primarily for educational and research purposes.
"""

from spotify2ytmusic import utils, backend


def main():
    """Example of how to use the migration research tools."""
    
    print("🎵 Spotify to YouTube Music Migration - Research Project")
    print("=" * 60)
    print("⚠️  This is a research project with known limitations")
    print("   Authentication may fail due to YouTube Music's security measures")
    print("   Success is not guaranteed for large-scale migrations")
    print("=" * 60)
    
    # 1. Check YTMusic connection
    print("\n1. Checking YTMusic connection...")
    if not utils.check_ytmusic_connection():
        print("❌ Cannot proceed without YTMusic connection")
        print("   This is expected if authentication has expired")
        print("   Re-run authentication setup if needed")
        return
    
    # 2. List Spotify playlists
    print("\n2. Listing Spotify playlists...")
    try:
        utils.list_spotify_playlists()
    except Exception as e:
        print(f"❌ Error listing playlists: {e}")
        print("   Make sure playlists.json exists and is valid")
    
    # 3. Example: Search for a song (this usually works)
    print("\n3. Example: Search for a song...")
    print("   This demonstrates the search functionality:")
    print("   python -m spotify2ytmusic search 'Bohemian Rhapsody' --artist 'Queen'")
    
    # 4. Example: Create a playlist (this usually works)
    print("\n4. Example: Create a new playlist...")
    print("   This demonstrates playlist creation:")
    print("   python -m spotify2ytmusic create_playlist 'My Research Playlist'")
    
    # 5. Example: Transfer liked songs (may fail due to auth issues)
    print("\n5. Example: Transfer liked songs...")
    print("   ⚠️  This may fail due to authentication limitations:")
    print("   python -m spotify2ytmusic load_liked --dry-run")
    print("   Use --dry-run first to test without making changes")
    
    # 6. Example: Transfer a specific playlist (may fail due to auth issues)
    print("\n6. Example: Transfer a specific playlist...")
    print("   ⚠️  This may fail due to authentication limitations:")
    print("   python -m spotify2ytmusic copy_playlist <spotify_id> <ytmusic_id> --dry-run")
    
    print("\n📚 Available commands:")
    print("   python -m spotify2ytmusic list_playlists")
    print("   python -m spotify2ytmusic search <song_name> --artist <artist>")
    print("   python -m spotify2ytmusic create_playlist <name>")
    print("   python -m spotify2ytmusic load_liked --dry-run")
    print("   python -m spotify2ytmusic copy_playlist <spotify_id> <ytmusic_id> --dry-run")
    
    print("\n🔬 Research Notes:")
    print("   - Start with small playlists (10-50 songs)")
    print("   - Always use --dry-run first")
    print("   - Re-authenticate when sessions expire")
    print("   - Manual verification is recommended")
    print("   - This tool serves as a starting point, not a complete solution")


if __name__ == "__main__":
    main() 