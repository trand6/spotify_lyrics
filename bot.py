import time 
import os
import re
import requests 

import spotipy

from string import digits
from lyricsgenius import Genius
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook, DiscordEmbed

##### ------------- TOKEN AUTHENTICATION ------------- #####
load_dotenv()

# spotify 
SPOTIPY_CLIENT_ID = os.getenv('spotify_id')
SPOTIPY_CLIENT_SECRET = os.getenv('spotify_secret')
scope = "user-read-currently-playing"

spotify0Auth = spotipy.SpotifyOAuth(client_id=os.getenv('spotify_id'),
                                    client_secret=os.getenv('spotify_secret'),
                                    redirect_uri=os.getenv('spotify_redirect_uri'),
                                    scope=scope)

# geniuslyrics
GENIUS_ACCESS_TOKEN = os.getenv("genius_access_token")
genius = Genius("genius_access_token")

##### ------------- DISCORD WEBHOOK ------------- #####
def webhook_print(title_track, artist, lyrics, genius_url=""):
    '''Print title track lyrics.'''
    webhook = DiscordWebhook(url=os.getenv('discord_webhook'))

    embed = DiscordEmbed(title=title_track, color=0x32CD32, description=lyrics)
    embed.set_author(name="Spotify Lyrics", url="https://open.spotify.com/", icon_url="https://www.freepnglogos.com/uploads/spotify-logo-png/spotify-download-logo-30.png")
    embed.set_footer(text=genius_url, icon_url="https://images.genius.com/0ca83e3130e1303a7f78ba351e3091cd.1000x1000x1.png")
    embed.add_embed_field(name=artist, value="_")

    # image of album
    # embed.set_image(url="")

    webhook.add_embed(embed)
    webhook.execute()

def no_lyrics():
    '''Print when no lyrics are found.'''
    webhook = DiscordWebhook(url=os.getenv('discord_webhook'))

    embed = DiscordEmbed(title="no lyrics for this song found", color=0x32CD32)
    embed.set_author(name="Spotify Lyrics", url="https://open.spotify.com/", icon_url="https://www.freepnglogos.com/uploads/spotify-logo-png/spotify-download-logo-30.png")
    
    webhook.add_embed(embed)
    webhook.execute()

def message(text):
    webhook = DiscordWebhook(url=os.getenv('discord_webhook'))

    embed = DiscordEmbed(title=text, color=0x32CD32)
    embed.set_author(name="Spotify Lyrics", url="https://open.spotify.com/", icon_url="https://www.freepnglogos.com/uploads/spotify-logo-png/spotify-download-logo-30.png")
    
    webhook.add_embed(embed)
    webhook.execute()

##### ------------- FUNCTIONS ------------- #####
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


def print_lyrics(song, title_track):
    """Returns lyrics of a song and displays on terminal."""
    try:
        lyrics = song.lyrics.replace("EmbedShare URLCopyEmbedCopy", "").rstrip(digits)
        lyrics = lyrics.replace("Embed", "")
        
    # if no lyrics are available from the title track and artist, search again without artist name
    except AttributeError:

        lyrics = genius.search_song(title=title_track)

        try:
            lyrics = song.lyrics.replace("EmbedShare URLCopyEmbedCopy", "").rstrip(digits)
            lyrics = lyrics.replace("Embed", "")

        except AttributeError:
            lyrics = "lyrics for this song not found"

    return lyrics


##### ------------- MAIN ------------- #####
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

                    # remove any words from remove_words in the song title
                    big_regex = re.compile('|'.join(map(re.escape, remove_words)))
                    title = big_regex.sub("", current_track_info["track_name"]).strip()

                    # look up lyrics using song title and artist name 
                    song = genius.search_song(title=title, artist=current_track_info["artist"])
                    
                    try:
                        artist = current_track_info['artists']
                        title_track = current_track_info['track_name']

                    except AttributeError:
                        message("lyrics for this song not found")

                    ### PRINT TO DISCORD CHANNEL ####
                    print(title_track)
                    print(artist)
                    lyrics = print_lyrics(song, title_track).rstrip(digits)
                    print(lyrics)
                    try:
                        webhook_print(title_track, artist, lyrics, song.url)
                    except AttributeError:
                        webhook_print(title_track, artist, lyrics)

                    #################################

                    current_track_id = current_track_info['id']

                # during advertisements, program will pause for 30 seconds
                elif current_type == "ad":
                    message("ad popped up -- sleeping for 30 seconds")
                    time.sleep(30)

            # if the song played is a local file, we will use the local file's title track and artist name
            except KeyError:
                if  local_track != current['item']['name']:
                    local_track = current['item']['name']
                    local_artist = current['item']['artists'][0]['name']
                    song = genius.search_song(title=local_track, artist=local_artist)
                    message(f"Currently playing local file:\n{local_track} - {local_artist}")

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
        message("powering off ...")
        print("\n>> powering off ...\n")



