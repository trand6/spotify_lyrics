# Spotify Lyrics :notes:

Automatically display currently playing Spotify lyrics to a Discord channel and terminal.

## About :musical_note:	
This Python program will use the spotipy library to get the title track and artist of the currently playing song. Then lyricsgenius will use that information to search the title track and artist to use a webhook and display the lyrics in a resizable terminal window.
![](demo.gif)


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

```bash
pip3 install discord_webhook
```
## Notes :bulb:
- The lyrics need to be available in Genius's music lyric database in order to be displayed.
- If the title track and artist yield no results, the program will try to search again without the artist to account for possible song covers and look for the original artist.
- Discord: Server Settings > Integration > Webhooks > New Webhook > Copy Webhook URL > paste into .env

Displaying the lyrics to both the Discord channel and terminal:
```bash
python3 run bot.py
```
Displaying lyrics to the terminal only:
```bash
python3 spotify_lyrics.py
```

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