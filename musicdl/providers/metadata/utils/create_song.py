from spotipy import Spotify
from musicdl.common import MusicDLException, Song

def create_song(spotify_client: Spotify, url: str) -> Song:
    raw_track_metadata = spotify_client.track(url)
        
    if raw_track_metadata is None:
        raise MusicDLException("Couldn't get metadata, check if you have passed correct track id")
    
    # get artist info
    primary_artist_id = raw_track_metadata["artists"][0]["id"]
    raw_artist_metadata: Dict[str, Any] = self._spotifyClient.artist(primary_artist_id)  # type: ignore

    # get album info
    album_id = raw_track_metadata["album"]["id"]
    raw_album_metadata: Dict[str, Any] = self._spotifyClient.album(album_id)  # type: ignore
    
    # create song object
    return Song(
        name=raw_track_metadata["name"],
        artists=[artist["name"] for artist in raw_track_metadata["artists"]],
        artist=raw_track_metadata["artists"][0]["name"],
        album_name=raw_album_metadata["name"],
        album_artist=raw_album_metadata["artists"][0]["name"],
        copyright_text=raw_album_metadata["copyrights"][0]["text"] if raw_album_metadata["copyrights"] else None,
        genres=raw_album_metadata["genres"] + raw_artist_metadata["genres"],
        disc_number=raw_track_metadata["disc_number"],
        disc_count=int(raw_album_metadata["tracks"]["items"][-1]["disc_number"]),
        duration=raw_track_metadata["duration_ms"] / 1000,
        year=int(raw_album_metadata["release_date"][:4]),
        date=raw_album_metadata["release_date"],
        track_number=raw_track_metadata["track_number"],
        tracks_count=raw_album_metadata["total_tracks"],
        isrc=raw_track_metadata.get("external_ids", {}).get("isrc"),
        song_id=raw_track_metadata["id"],
        explicit=raw_track_metadata["explicit"],
        publisher=raw_album_metadata["label"],
        url=raw_track_metadata["external_urls"]["spotify"],
        cover_url=max(raw_album_metadata["images"], key=lambda i: i["width"] * i["height"])["url"] if raw_album_metadata["images"] else None,
    )