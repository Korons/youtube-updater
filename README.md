## Install

To Install the program run `./install.sh`

Or if you want to do it all by hand

```
mkdir -p ~/.config/youtube-updater/
touch ~/.config/youtube-updater/downloaded.txt
touch ~/.config/youtube-updater/channels.txt
```

## Configuration

The default path for the Configuration files are `~/.config/youtube-updater/channels.txt` and `~/.config/youtube-updater/downloaded.txt`.

You can change the paths by editing the 9th and 10th lines in youtube-updater.py

To add a channel open `~/.config/youtube-updater/channels.txt` with a text editor and add `https://www.youtube.com/feeds/videos.xml?user=USERNAME` where USERNAME is the username of the channel you want to follow, or `https://www.youtube.com/feeds/videos.xml?channel_id=CHANNELID` where CHANNELID is the channel id of the channel you want to follow.

## Requirements

The only requirement is feedparser which can be installed with

`sudo pip3 install feedparser`

## Usage

Run the program with `python3 youtube-updater.py`.
