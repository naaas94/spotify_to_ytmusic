#!/usr/bin/env python3

"""
Example usage of the optimized Spotify to YouTube Music migration tools.
"""

from spotify2ytmusic import utils, backend


def main():
    """Example of how to use the optimized migration tools."""
    
    print("🎵 Spotify to YouTube Music Migration - Example Usage")
    print("=" * 60)
    
    # 1. Check YTMusic connection
    print("\n1. Checking YTMusic connection...")
    if not utils.check_ytmusic_connection():
        print("❌ Cannot proceed without YTMusic connection")
        return
    
    # 2. List Spotify playlists
    print("\n2. Listing Spotify playlists...")
    utils.list_spotify_playlists()
    
    # 3. Example: Transfer a specific playlist
    print("\n3. Example: Transfer a playlist by name...")
    example_playlists = ["Chill", "Lounge"]  # Replace with your playlist names
    
    # This would transfer the playlists (commented out for safety)
    # results = utils.batch_transfer_playlists(example_playlists, track_sleep=0.5, dry_run=True)
    
    print("   (Transfer commented out for safety - uncomment to run)")
    
    # 4. Example: Transfer liked songs
    print("\n4. Example: Transfer liked songs...")
    print("   Run: python -m spotify2ytmusic load_liked --dry-run")
    
    # 5. Example: Search for a song
    print("\n5. Example: Search for a song...")
    print("   Run: python -m spotify2ytmusic search 'Bohemian Rhapsody' --artist 'Queen'")
    
    # 6. Example: Create a new playlist
    print("\n6. Example: Create a new playlist...")
    print("   Run: python -m spotify2ytmusic create_playlist 'My New Playlist'")
    
    print("\n✅ Example completed!")
    print("\n📚 Available commands:")
    print("   python -m spotify2ytmusic list_playlists")
    print("   python -m spotify2ytmusic load_liked")
    print("   python -m spotify2ytmusic copy_playlist <spotify_id> <ytmusic_id>")
    print("   python -m spotify2ytmusic copy_all_playlists")
    print("   python -m spotify2ytmusic search <song_name> --artist <artist>")
    print("   python -m spotify2ytmusic create_playlist <name>")


if __name__ == "__main__":
    main() 