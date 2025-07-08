#!/usr/bin/env python3

import json
import sys
import os
import time
import re
from typing import Optional, Union, Iterator, Dict, List, Any
from collections import namedtuple
from dataclasses import dataclass, field

from ytmusicapi import YTMusic

SongInfo = namedtuple("SongInfo", ["title", "artist", "album"])


@dataclass
class ResearchDetails:
    """Details about song search research."""
    query: Optional[str] = field(default=None)
    songs: Optional[List[Dict[str, Any]]] = field(default=None)
    suggestions: Optional[List[str]] = field(default=None)


class YTMusicError(Exception):
    """Custom exception for YTMusic related errors."""
    pass


def get_ytmusic() -> YTMusic:
    """
    Initialize and return YTMusic client using oauth.json credentials.
    
    Returns:
        YTMusic: Configured YTMusic client
        
    Raises:
        SystemExit: If oauth.json is missing or invalid
    """
    if not os.path.exists("oauth.json"):
        print("ERROR: No file 'oauth.json' exists in the current directory.")
        print("       Have you logged in to YTMusic?  Run 'ytmusicapi oauth' to login")
        sys.exit(1)

    try:
        return YTMusic("oauth.json")
    except json.decoder.JSONDecodeError as e:
        print(f"ERROR: JSON Decode error while trying start YTMusic: {e}")
        print("       This typically means a problem with a 'oauth.json' file.")
        print("       Have you logged in to YTMusic?  Run 'ytmusicapi oauth' to login")
        sys.exit(1)


def _ytmusic_create_playlist(
    yt: YTMusic, title: str, description: str, privacy_status: str = "PRIVATE"
) -> str:
    """
    Create a playlist on YTMusic with retry logic.
    
    Args:
        yt: YTMusic client
        title: Playlist title
        description: Playlist description
        privacy_status: Privacy setting (PRIVATE, PUBLIC, UNLISTED)
        
    Returns:
        str: Playlist ID
        
    Raises:
        YTMusicError: If playlist creation fails after retries
    """
    def _create() -> Union[str, Dict[str, str]]:
        exception_sleep = 5
        for attempt in range(10):
            try:
                playlist_id = yt.create_playlist(
                    title=title, description=description, privacy_status=privacy_status
                )
                return playlist_id
            except Exception as e:
                print(
                    f"ERROR: (Retrying create_playlist: {title}) {e} in {exception_sleep} seconds"
                )
                if attempt < 9:  # Don't sleep on last attempt
                    time.sleep(exception_sleep)
                    exception_sleep *= 2

        return {
            "s2yt error": f'ERROR: Could not create playlist "{title}" after multiple retries'
        }

    result = _create()
    if isinstance(result, dict):
        raise YTMusicError(f"Failed to create playlist (name: {title}): {result}")

    time.sleep(1)  # Needed to avoid missing playlist ID error
    return result


def load_playlists_json(filename: str = "playlists.json", encoding: str = "utf-8") -> Dict[str, Any]:
    """Load the playlists.json Spotify playlist file."""
    try:
        with open(filename, "r", encoding=encoding) as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Playlist file '{filename}' not found")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in '{filename}': {e}", e.doc, e.pos)


def create_playlist(pl_name: str, privacy_status: str = "PRIVATE") -> None:
    """
    Create a YTMusic playlist.
    
    Args:
        pl_name: The name of the playlist to create
        privacy_status: Privacy setting (PRIVATE, PUBLIC, UNLISTED)
    """
    if not pl_name.strip():
        raise ValueError("Playlist name cannot be empty")
        
    yt = get_ytmusic()
    playlist_id = _ytmusic_create_playlist(
        yt, title=pl_name, description=pl_name, privacy_status=privacy_status
    )
    print(f"Playlist ID: {playlist_id}")


def iter_spotify_liked_albums(
    spotify_playlist_file: str = "playlists.json",
    spotify_encoding: str = "utf-8",
) -> Iterator[SongInfo]:
    """Yield songs from liked albums on Spotify."""
    spotify_pls = load_playlists_json(spotify_playlist_file, spotify_encoding)

    if "albums" not in spotify_pls:
        return

    for album in [x["album"] for x in spotify_pls["albums"]]:
        for track in album["tracks"]["items"]:
            yield SongInfo(track["name"], track["artists"][0]["name"], album["name"])


def iter_spotify_playlist(
    src_pl_id: Optional[str] = None,
    spotify_playlist_file: str = "playlists.json",
    spotify_encoding: str = "utf-8",
    reverse_playlist: bool = True,
) -> Iterator[SongInfo]:
    """
    Yield songs from a specific Spotify playlist.
    
    Args:
        src_pl_id: Spotify playlist ID (None for "Liked Songs")
        spotify_playlist_file: Path to playlists backup file
        spotify_encoding: Character encoding
        reverse_playlist: If True, reverse playlist order
        
    Yields:
        SongInfo: Song information
    """
    spotify_pls = load_playlists_json(spotify_playlist_file, spotify_encoding)

    def find_spotify_playlist(spotify_pls: Dict[str, Any], src_pl_id: Optional[str]) -> Dict[str, Any]:
        """Find Spotify playlist by ID or name."""
        for src_pl in spotify_pls["playlists"]:
            if src_pl_id is None and str(src_pl.get("name")) == "Liked Songs":
                return src_pl
            if src_pl_id is not None and str(src_pl.get("id")) == src_pl_id:
                return src_pl
        raise ValueError(f"Could not find Spotify playlist {src_pl_id}")

    src_pl = find_spotify_playlist(spotify_pls, src_pl_id)
    src_pl_name = src_pl["name"]
    print(f"== Spotify Playlist: {src_pl_name}")

    pl_tracks = src_pl["tracks"]
    if reverse_playlist:
        pl_tracks = reversed(pl_tracks)

    for src_track in pl_tracks:
        if src_track["track"] is None:
            print(f"WARNING: Spotify track seems to be malformed, Skipping. Track: {src_track!r}")
            continue

        try:
            src_album_name = src_track["track"]["album"]["name"]
            src_track_artist = src_track["track"]["artists"][0]["name"]
        except (TypeError, KeyError) as e:
            print(f"ERROR: Spotify track seems to be malformed. Track: {src_track!r}")
            raise e
            
        src_track_name = src_track["track"]["name"]
        yield SongInfo(src_track_name, src_track_artist, src_album_name)


def get_playlist_id_by_name(yt: YTMusic, title: str) -> Optional[str]:
    """
    Look up a YTMusic playlist ID by name.
    
    Args:
        yt: YTMusic client
        title: Playlist title
        
    Returns:
        Optional[str]: Playlist ID or None if not found
    """
    try:
        playlists = yt.get_library_playlists(limit=5000)
    except KeyError as e:
        print("=" * 60)
        print(f"Attempting to look up playlist '{title}' failed with KeyError: {e}")
        print("This is a bug in ytmusicapi that prevents 'copy_all_playlists' from working.")
        print("You will need to manually copy playlists using s2yt_list_playlists and s2yt_copy_playlist")
        print("until this bug gets resolved. Try `pip install --upgrade ytmusicapi` just to verify")
        print("you have the latest version of that library.")
        print("=" * 60)
        raise

    for pl in playlists:
        if pl["title"] == title:
            return pl["playlistId"]

    return None


def lookup_song(
    yt: YTMusic,
    track_name: str,
    artist_name: str,
    album_name: str,
    yt_search_algo: int,
    details: Optional[ResearchDetails] = None,
) -> Dict[str, Any]:
    """
    Look up a song on YTMusic using various search algorithms.
    
    Args:
        yt: YTMusic client
        track_name: Track name
        artist_name: Artist name
        album_name: Album name
        yt_search_algo: Search algorithm (0=exact, 1=extended, 2=approximate)
        details: Optional research details object
        
    Returns:
        Dict[str, Any]: Song information
        
    Raises:
        ValueError: If no track is found
    """
    # Try to find exact match in album first
    albums = yt.search(query=f"{album_name} by {artist_name}", filter="albums")
    for album in albums[:3]:
        try:
            for track in yt.get_album(album["browseId"])["tracks"]:
                if track["title"] == track_name:
                    return track
        except Exception as e:
            print(f"Unable to lookup album ({e}), continuing...")

    # Fallback to song search
    query = f"{track_name} by {artist_name}"
    if details:
        details.query = query
        suggestions = yt.get_search_suggestions(query=query)
        details.suggestions = [s for s in suggestions if isinstance(s, str)]
        
    songs = yt.search(query=query, filter="songs")

    match yt_search_algo:
        case 0:  # Exact match
            if details:
                details.songs = songs
            return songs[0]

        case 1:  # Extended match
            for song in songs:
                if (
                    song["title"] == track_name
                    and song["artists"][0]["name"] == artist_name
                    and song["album"]["name"] == album_name
                ):
                    return song
            raise ValueError(f"Did not find {track_name} by {artist_name} from {album_name}")

        case 2:  # Approximate match
            for song in songs:
                # Remove everything in brackets in the song title
                song_title_without_brackets = re.sub(r"[\[(].*?[])]", "", song["title"])
                if (
                    (
                        song_title_without_brackets == track_name
                        and song["album"]["name"] == album_name
                    )
                    or (song_title_without_brackets == track_name)
                    or (song_title_without_brackets in track_name)
                    or (track_name in song_title_without_brackets)
                ) and (
                    song["artists"][0]["name"] == artist_name
                    or artist_name in song["artists"][0]["name"]
                ):
                    return song

            # Try video search as last resort
            track_name_lower = track_name.lower()
            first_song_title = songs[0]["title"].lower()
            if (
                track_name_lower not in first_song_title
                or songs[0]["artists"][0]["name"] != artist_name
            ):
                print("Not found in songs, searching videos")
                videos = yt.search(query=f"{track_name} by {artist_name}", filter="videos")

                for video in videos:
                    video_title = video["title"].lower()
                    if (
                        track_name_lower in video_title
                        and artist_name.lower() in video_title
                    ) or (track_name_lower in video_title):
                        print("Found a video")
                        return video
                else:
                    raise ValueError(f"Did not find {track_name} by {artist_name} from {album_name}")
            else:
                return songs[0]

        case _:
            raise ValueError(f"Invalid search algorithm: {yt_search_algo}")


def copier(
    src_tracks: Iterator[SongInfo],
    dst_pl_id: Optional[str] = None,
    dry_run: bool = False,
    track_sleep: float = 0.1,
    yt_search_algo: int = 0,
    *,
    yt: Optional[YTMusic] = None,
) -> None:
    """
    Copy tracks from Spotify to YouTube Music.
    
    Args:
        src_tracks: Iterator of Spotify tracks to copy
        dst_pl_id: YouTube Music playlist ID (None for Liked Songs)
        dry_run: If True, don't actually add tracks
        track_sleep: Sleep time between track additions
        yt_search_algo: Search algorithm (0=exact, 1=extended, 2=approximate)
        yt: YTMusic client (auto-initialized if None)
    """
    if yt is None:
        yt = get_ytmusic()

    if dst_pl_id is not None:
        try:
            yt_pl = yt.get_playlist(playlistId=dst_pl_id)
            print(f"== Youtube Playlist: {yt_pl['title']}")
        except Exception as e:
            print(f"ERROR: Unable to find YTMusic playlist {dst_pl_id}: {e}")
            print("       Make sure the YTMusic playlist ID is correct, it should be something like")
            print("      'PL_DhcdsaJ7echjfdsaJFhdsWUd73HJFca'")
            sys.exit(1)

    tracks_added_set = set()
    duplicate_count = 0
    error_count = 0

    for src_track in src_tracks:
        print(f"Spotify:   {src_track.title} - {src_track.artist} - {src_track.album}")

        try:
            dst_track = lookup_song(
                yt, src_track.title, src_track.artist, src_track.album, yt_search_algo
            )
        except Exception as e:
            print(f"ERROR: Unable to look up song on YTMusic: {e}")
            error_count += 1
            continue

        yt_artist_name = "<Unknown>"
        if "artists" in dst_track and len(dst_track["artists"]) > 0:
            yt_artist_name = dst_track["artists"][0]["name"]
        print(
            f"  Youtube: {dst_track['title']} - {yt_artist_name} - {dst_track.get('album', '<Unknown>')}"
        )

        if dst_track["videoId"] in tracks_added_set:
            print("(DUPLICATE, this track has already been added)")
            duplicate_count += 1
        tracks_added_set.add(dst_track["videoId"])

        if not dry_run:
            exception_sleep = 5
            for _ in range(10):
                try:
                    if dst_pl_id is not None:
                        yt.add_playlist_items(
                            playlistId=dst_pl_id,
                            videoIds=[dst_track["videoId"]],
                            duplicates=False,
                        )
                    else:
                        yt.rate_song(dst_track["videoId"], "LIKE")
                    break
                except Exception as e:
                    print(
                        f"ERROR: (Retrying add_playlist_items: {dst_pl_id} {dst_track['videoId']}) {e} in {exception_sleep} seconds"
                    )
                    time.sleep(exception_sleep)
                    exception_sleep *= 2

        if track_sleep:
            time.sleep(track_sleep)

    print()
    print(
        f"Added {len(tracks_added_set)} tracks, encountered {duplicate_count} duplicates, {error_count} errors"
    )


def copy_playlist(
    spotify_playlist_id: str,
    ytmusic_playlist_id: str,
    spotify_playlists_encoding: str = "utf-8",
    dry_run: bool = False,
    track_sleep: float = 0.1,
    yt_search_algo: int = 0,
    reverse_playlist: bool = True,
    privacy_status: str = "PRIVATE",
) -> None:
    """
    Copy a Spotify playlist to a YTMusic playlist.
    
    Args:
        spotify_playlist_id: Spotify playlist ID
        ytmusic_playlist_id: YouTube Music playlist ID or name (prefix with + for name)
        spotify_playlists_encoding: Encoding of playlists.json file
        dry_run: If True, don't actually add tracks
        track_sleep: Sleep time between track additions
        yt_search_algo: Search algorithm (0=exact, 1=extended, 2=approximate)
        reverse_playlist: If True, reverse playlist order
        privacy_status: Playlist privacy setting
    """
    print(f"Using search algorithm: {yt_search_algo}")
    yt = get_ytmusic()
    pl_name: str = ""

    if ytmusic_playlist_id.startswith("+"):
        pl_name = ytmusic_playlist_id[1:]
        ytmusic_playlist_id = get_playlist_id_by_name(yt, pl_name)
        print(f"Looking up playlist '{pl_name}': id={ytmusic_playlist_id}")

    if ytmusic_playlist_id is None:
        if pl_name == "":
            print("No playlist name or ID provided, creating playlist...")
            spotify_pls = load_playlists_json()
            for pl in spotify_pls["playlists"]:
                if len(pl.keys()) > 3 and pl["id"] == spotify_playlist_id:
                    pl_name = pl["name"]
                    break

        if not pl_name:
            pl_name = f"Spotify Playlist {spotify_playlist_id}"

        ytmusic_playlist_id = _ytmusic_create_playlist(
            yt, title=pl_name, description=pl_name, privacy_status=privacy_status
        )
        print(f"NOTE: Created playlist '{pl_name}' with ID: {ytmusic_playlist_id}")

    copier(
        iter_spotify_playlist(
            spotify_playlist_id,
            spotify_encoding=spotify_playlists_encoding,
            reverse_playlist=reverse_playlist,
        ),
        ytmusic_playlist_id,
        dry_run,
        track_sleep,
        yt_search_algo,
        yt=yt,
    )


def copy_all_playlists(
    track_sleep: float = 0.1,
    dry_run: bool = False,
    spotify_playlists_encoding: str = "utf-8",
    yt_search_algo: int = 0,
    reverse_playlist: bool = True,
    privacy_status: str = "PRIVATE",
) -> None:
    """
    Copy all Spotify playlists (except Liked Songs) to YTMusic playlists.
    
    Args:
        track_sleep: Sleep time between track additions
        dry_run: If True, don't actually add tracks
        spotify_playlists_encoding: Encoding of playlists.json file
        yt_search_algo: Search algorithm (0=exact, 1=extended, 2=approximate)
        reverse_playlist: If True, reverse playlist order
        privacy_status: Playlist privacy setting
    """
    spotify_pls = load_playlists_json()
    yt = get_ytmusic()

    for src_pl in spotify_pls["playlists"]:
        if str(src_pl.get("name")) == "Liked Songs":
            continue

        pl_name = src_pl["name"]
        if pl_name == "":
            pl_name = f"Unnamed Spotify Playlist {src_pl['id']}"

        dst_pl_id = get_playlist_id_by_name(yt, pl_name)
        print(f"Looking up playlist '{pl_name}': id={dst_pl_id}")
        
        if dst_pl_id is None:
            dst_pl_id = _ytmusic_create_playlist(
                yt, title=pl_name, description=pl_name, privacy_status=privacy_status
            )
            print(f"NOTE: Created playlist '{pl_name}' with ID: {dst_pl_id}")

        copier(
            iter_spotify_playlist(
                src_pl["id"],
                spotify_encoding=spotify_playlists_encoding,
                reverse_playlist=reverse_playlist,
            ),
            dst_pl_id,
            dry_run,
            track_sleep,
            yt_search_algo,
        )
        print("\nPlaylist done!\n")

    print("All done!") 