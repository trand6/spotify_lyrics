# Spotify Lyrics :notes:

Automatically display music lyrics on the terminal to the song you're listening to from Spotify.

## About :musical_note:	
This Python program will use the spotipy library to get the title track and artist of the currently playing song.Then lyricsgenius will use that information to search the title track and artist to display the lyrics in a resizable terminal window.
![](spotify_lyrics_demo.gif)
## Installation :desktop_computer:

```bash
pip3 install lyricsgenius
```
```bash
pip3 install spotipy
```
```bash
pip3 install python-dotenv
```
## Notes :bulb:
- The lyrics need to be available in Genius's music lyric database to be displayed.
- If the title track and artist yield no results, the program will try to search again without the artist to account for possible song covers and look for the original artist.

## Documentation :book:
Check out these important documents to properly set up authorization:
- [lyricsgenius](https://lyricsgenius.readthedocs.io/en/master/setup.html)
- [spotipy](https://spotipy.readthedocs.io/en/2.19.0/)


## Acknowldegements :star2:
Thank you for the inspirational tutorials to help me get started:

Imdad Codes:
[Get Currently Playing Track With Spotify API (Python Tutorial)](https://www.youtube.com/watch?v=yKz38ThJWqE)

Elbert:
[How to automate with Python, Spotipy, and LyricsGenius](https://www.youtube.com/watch?v=cU8YH2rhN6A)