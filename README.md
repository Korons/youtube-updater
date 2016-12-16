## Installing on Nix

To Install the program run `./install.sh` if on MacOS or linux

Or if you want to do it all by hand

```
mkdir -p ~/.config/youtube-updater/
touch ~/.config/youtube-updater/downloaded.txt
touch ~/.config/youtube-updater/channels.txt
```

## Installing on windows

Make a folder inside the folder where you downloaded this script named .config/youtube-updater/

inside `youtube-updater/.config/youtube-updater/` make 2 text files with the names `downloaded.txt` and `channels.txt`

Inside of `youtube-updater` make a folder called Videos

## Configuration

The default path for the Configuration files are `~/.config/youtube-updater/channels.txt` and `~/.config/youtube-updater/downloaded.txt`.

To add a channel open `~/.config/youtube-updater/channels.txt` with a text editor and add `https://www.youtube.com/feeds/videos.xml?user=USERNAME` where USERNAME is the username of the channel you want to follow, or `https://www.youtube.com/feeds/videos.xml?channel_id=CHANNELID` where CHANNELID is the channel id of the channel you want to follow.

## Requirements

You need feedparser which can be installed with

`pip3 install feedparser`

And youtube-dl which can be installed with

`pip3 install youtube-dl`

## Usage

Run the program with `python3 youtube-updater.py`.
