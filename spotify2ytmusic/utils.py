#!/usr/bin/env python3

"""
Utility functions for Spotify to YouTube Music migration.
"""

import json
import subprocess
import time
from typing import List, Dict, Any, Optional
from . import backend


def check_ytmusic_connection() -> bool:
    """
    Check if YTMusic connection is working and show basic info.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        yt = backend.get_ytmusic()
        
        # Get liked songs
        liked_songs = yt.get_liked_songs(limit=10)
        tracks = liked_songs.get('tracks', []) if isinstance(liked_songs, dict) else liked_songs
        
        print(f"✅ YTMusic connection successful")
        print(f"📊 Found {len(tracks)} liked songs")
        
        if tracks:
            print("🎵 Recent liked songs:")
            for i, song in enumerate(tracks[:5]):
                print(f"  {i+1}. {song['title']} - {song['artists'][0]['name']}")
        
        # Get playlists
        playlists = yt.get_library_playlists(limit=10)
        print(f"\n📋 Found {len(playlists)} playlists in library")
        
        return True
        
    except Exception as e:
        print(f"❌ YTMusic connection failed: {e}")
        return False


def convert_spotify_library_to_playlists(
    library_file: str = "YourLibrary.json",
    output_file: str = "playlists.json"
) -> None:
    """
    Convert Spotify library format to playlists format.
    
    Args:
        library_file: Path to YourLibrary.json file
        output_file: Output playlists.json file
    """
    try:
        with open(library_file, 'r', encoding='utf-8') as f:
            library_data = json.load(f)
        
        # Create liked songs playlist
        liked_playlist = {
            'id': 'liked_songs',
            'name': 'Liked Songs',
            'tracks': []
        }
        
        for track in library_data.get('tracks', []):
            liked_playlist['tracks'].append({
                'track': {
                    'name': track.get('track', ''),
                    'artists': [{'name': track.get('artist', '')}],
                    'album': {'name': track.get('album', '')},
                    'uri': track.get('uri', '')
                }
            })
        
        # Load existing playlists or create new structure
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                playlists_data = json.load(f)
        except FileNotFoundError:
            playlists_data = {'playlists': []}
        
        # Add liked songs at the beginning
        playlists_data['playlists'].insert(0, liked_playlist)
        
        # Save updated file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(playlists_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Converted {len(liked_playlist['tracks'])} liked songs to {output_file}")
        
    except Exception as e:
        print(f"❌ Error converting library: {e}")


def convert_playlist_format(
    input_file: str = "Playlist1.json",
    output_file: str = "playlists.json"
) -> None:
    """
    Convert old playlist format to new format.
    
    Args:
        input_file: Input playlist file
        output_file: Output playlists.json file
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        converted = {'playlists': []}
        
        for playlist in data.get('playlists', []):
            new_playlist = {
                'id': playlist.get('id', ''),
                'name': playlist['name'],
                'tracks': []
            }
            
            for item in playlist.get('items', []):
                track = item.get('track')
                if track:
                    new_playlist['tracks'].append({
                        'track': {
                            'name': track.get('trackName', ''),
                            'artists': [{'name': track.get('artistName', '')}],
                            'album': {'name': track.get('albumName', '')},
                            'uri': track.get('trackUri', '')
                        }
                    })
            
            converted['playlists'].append(new_playlist)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(converted, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Converted {len(converted['playlists'])} playlists to {output_file}")
        
    except Exception as e:
        print(f"❌ Error converting playlists: {e}")


def batch_transfer_playlists(
    playlist_names: List[str],
    track_sleep: float = 0.5,
    dry_run: bool = False
) -> Dict[str, bool]:
    """
    Transfer multiple playlists by name.
    
    Args:
        playlist_names: List of playlist names to transfer
        track_sleep: Sleep time between tracks
        dry_run: If True, don't actually transfer
        
    Returns:
        Dict[str, bool]: Mapping of playlist name to success status
    """
    results = {}
    
    print(f"🚀 Starting batch transfer of {len(playlist_names)} playlists...")
    
    for i, playlist_name in enumerate(playlist_names, 1):
        print(f"\n[{i}/{len(playlist_names)}] 🔄 Processing: {playlist_name}")
        
        try:
            # Create playlist if it doesn't exist
            subprocess.run([
                "python", "-m", "spotify2ytmusic", "create_playlist", playlist_name
            ], check=True, capture_output=True, text=True)
            
            # Transfer songs
            subprocess.run([
                "python", "-m", "spotify2ytmusic", "copy_playlist",
                "", f"+{playlist_name}",
                "--track-sleep", str(track_sleep),
                "--dry-run" if dry_run else ""
            ], check=True)
            
            results[playlist_name] = True
            print(f"✅ {playlist_name} completed successfully")
            
        except subprocess.CalledProcessError as e:
            results[playlist_name] = False
            print(f"❌ {playlist_name} failed: {e}")
        
        # Pause between playlists
        if i < len(playlist_names):
            time.sleep(2)
    
    # Summary
    successful = sum(results.values())
    failed = len(results) - successful
    
    print(f"\n🎉 Batch transfer completed:")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {len(results)}")
    
    return results


def transfer_playlist_by_id(
    spotify_playlist_id: str,
    ytmusic_playlist_id: str,
    track_sleep: float = 0.5,
    dry_run: bool = False
) -> bool:
    """
    Transfer a single playlist by ID.
    
    Args:
        spotify_playlist_id: Spotify playlist ID
        ytmusic_playlist_id: YouTube Music playlist ID
        track_sleep: Sleep time between tracks
        dry_run: If True, don't actually transfer
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"🔄 Transferring playlist {spotify_playlist_id} to {ytmusic_playlist_id}")
        
        subprocess.run([
            "python", "-m", "spotify2ytmusic", "copy_playlist",
            spotify_playlist_id, ytmusic_playlist_id,
            "--track-sleep", str(track_sleep),
            "--dry-run" if dry_run else ""
        ], check=True)
        
        print(f"✅ Transfer completed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Transfer failed: {e}")
        return False


def get_spotify_playlists() -> List[Dict[str, Any]]:
    """
    Get list of Spotify playlists from playlists.json.
    
    Returns:
        List[Dict[str, Any]]: List of playlist information
    """
    try:
        playlists_data = backend.load_playlists_json()
        return playlists_data.get('playlists', [])
    except Exception as e:
        print(f"❌ Error loading playlists: {e}")
        return []


def list_spotify_playlists() -> None:
    """List all Spotify playlists with their track counts."""
    playlists = get_spotify_playlists()
    
    if not playlists:
        print("❌ No playlists found")
        return
    
    print("📋 Spotify Playlists:")
    print("-" * 60)
    
    for i, playlist in enumerate(playlists, 1):
        track_count = len(playlist.get('tracks', []))
        print(f"{i:2d}. {playlist['name']:40} ({track_count:3d} tracks) - ID: {playlist.get('id', 'N/A')}")
    
    print(f"\nTotal: {len(playlists)} playlists") 