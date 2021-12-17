import time
import os
import string
import re
import requests

import spotipy 
from lyricsgenius import Genius
from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('spotify_id')
SPOTIPY_CLIENT_SECRET = os.getenv('spotify_secret')
scope = "user-read-currently-playing"

spotify0Auth = spotipy.SpotifyOAuth(client_id=os.getenv('spotify_id'),
                                    client_secret=os.getenv('spotify_secret'),
                                    redirect_uri=os.getenv('spotify_redirect_uri'),
                                    scope=scope)

# retrieve genius token and declare genius object
GENIUS_ACCESS_TOKEN = os.getenv("genius_access_token")
genius = Genius("genius_access_token")

def get_current_track(current):
    """Returns current song's info in a dictionary."""
    track_id = current['item']['id']    
    track_name = current['item']['name']
    artist = current['item']['artists'][0]['name']
    artists = [artist for artist in current['item']['artists']]
    artist_names = ', '.join([artist['name'] for artist in artists])
    link = current['item']['external_urls']['spotify']

    current_track_info = {
        "id": track_id,
        "track_name": track_name,
        "artist": artist,
        "artists": artist_names,
        "link": link
    }

    return current_track_info

def title_by_artist(current_track_info):
    """Returns official song title and artist name in the format of:
        song_title - artist"""
    try:
        artist_names = current_track_info['artists']
        song_title = current_track_info['track_name']
        heading = f"{song_title} - {artist_names}\n"

    except AttributeError:
        print("\n>> lyrics for this song not found \n")
        heading = ""
    
    return heading

def print_lyrics(song, title, heading=""):
    """Returns lyrics of a song and displays on terminal."""
    try:
        lyrics = song.lyrics.replace("EmbedShare URLCopyEmbedCopy", "").rstrip(string.digits)
        print(f"\n{heading}\n{lyrics}\n")

    except AttributeError:
        print()
        song = genius.search_song(title=title)

        try:
            lyrics = song.lyrics.replace("EmbedShare URLCopyEmbedCopy", "").rstrip(string.digits)
            print(f"\n{heading}\n{lyrics}\n")
            
            try:
                print(f"Currently playing: {song.title} - {song.artist}\n")
                print(f"Genius: {song.url}")
            except AttributeError:
                pass

        except AttributeError:
            print("\n>> lyrics for this song not found\n")
        
 
def main():
    # current official spotify track id
    current_track_id = None

    # track from your local files being played on spotify
    local_track = None

    # retrieve spotify token and declare spotify object
    token = spotify0Auth.get_cached_token()
    spotifyObject = spotipy.Spotify(auth=token['access_token'])

    # characters to remove from special song titles to make searching lyrics smoother
    remove_words = ['-', '(', ')', 'Live', 'Lofi', '(Lofi Ver.)', 'Version', 'Remix', 'Ver.', 'feat.']

    while True:

        # refreshes spotify auth token when expired
        if spotify0Auth.is_token_expired(token) == True:
            print("\n>> access token has expired -- refreshing ...\n")

            token = spotify0Auth.get_cached_token()
            spotifyObject = spotipy.Spotify(auth=token['access_token'])
    
        else:
            try:
                current = spotifyObject.currently_playing()
                current_type = current['currently_playing_type']
                current_track_info = get_current_track(current)

                if current_type == "track" and current_track_info['id'] != current_track_id:
                    print("============================================================")
                    big_regex = re.compile('|'.join(map(re.escape, remove_words)))
                    title = big_regex.sub("", current_track_info["track_name"]).strip()
                    song = genius.search_song(title=title, artist=current_track_info["artist"])
                    heading = title_by_artist(current_track_info)
                    print_lyrics(song, title, heading)
                    current_track_id = current_track_info['id']

                    try:
                        print(f"Currently playing: {song.title} - {song.artist}\n")
                        print(f"Genius: {song.url}")
                    except AttributeError:
                        pass

                    print(f"Spotify: {current_track_info['link']}")

                # during advertisements, program will pause for 30 seconds
                elif current_type == "ad":
                    print(">>ad popped up -- sleeping for 30 seconds")
                    time.sleep(30)

            # if the song played is a local file, we will use the local file's title track and artist name
            except KeyError:
                if  local_track != current['item']['name']:
                    local_track = current['item']['name']
                    local_artist = current['item']['artists'][0]['name']
                    song = genius.search_song(title=local_track, artist=local_artist)
                    print(f"Currently playing: {local_track} - {local_artist}")

            # continue program if there is NoneType 
            except TypeError:
                pass

            except requests.exceptions.Timeout:
                print("\n>> program timed out, restarting...\n")

        time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt: # ctrl + c to end program
        print("\n>> spotify lyrics script terminated\n")

# clean up code
