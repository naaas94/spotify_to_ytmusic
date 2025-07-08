# Spotify to YouTube Music Migrator (Failed Project)

## Purpose

The goal of this project was to migrate playlists and songs from Spotify to YouTube Music automatically, using reverse engineering and the `ytmusicapi` library.

## What the code does

- Allows you to export playlists and songs from Spotify to local files.
- Attempts to create playlists and add songs to YouTube Music using headers/cookies manually extracted from your browser session.
- Includes scripts for backup, playlist reversal, and a basic graphical interface.

## Technical limitations and why it fails

- **There is no official YouTube Music API for adding songs.** Everything relies on reverse engineering and session headers/cookies.
- **Headers/cookies expire very quickly** (sometimes in minutes), so authentication may "appear" to work but does not actually allow adding songs.
- **The `ytmusicapi` library and YouTube Music's internal API change frequently,** breaking scripts that previously worked.
- **There is no clear error feedback:** the API may respond "OK" but not actually add anything, and the script cannot detect this.
- **It is not possible to reliably and automatically migrate large numbers of songs (e.g., 5,000) at this time.**
- **Paid services face the same technical limitations,** though they may achieve better results due to infrastructure and maintenance, but they are not 100% reliable either.

## Current state

- The code can export your playlists and songs to local files (CSV/TXT/JSON).
- It is not possible to guarantee automatic, large-scale migration to YouTube Music.
- This project is not recommended for real migrations until there is an official API or a more robust solution.

## Privacy warning

**Do not upload files containing headers, cookies, tokens, or personal data to any public repository.**

## Files removed for security

- `headers_auth.json`, `oauth.json`, `playlists.json`, `playlists.json.backup`, and any other file containing sensitive data have been deleted.
- A safe example is provided: `headers_auth.json.example`.

## Conclusion

This project demonstrates the limits of automation when relying on unofficial APIs and closed platforms. It may serve as a technical reference, but **it is not a viable solution for migrating music between platforms at this time**.

---

**If Google releases an official API in the future, or the community finds a more robust method, this project could be revived.**
