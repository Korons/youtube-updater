#!/usr/bin/python3

import os
import sys
import feedparser
import youtube_dl
import argparse

parser = argparse.ArgumentParser(description='Download youtube videos')
parser.add_argument("-l", help="Log video titles to file", nargs='?')
args = parser.parse_args()

home = os.getenv("HOME")
path = '{0}/Videos'.format(home)
channels = '{0}/.config/youtube-updater/channels.txt'.format(home)
downloaded = '{0}/.config/youtube-updater/downloaded.txt'.format(home)

# We check if $HOME is set on the system

if home == None:
    print("$HOME is not set on this system")
    print("Using install dir as home")
    home = os.path.dirname(os.path.realpath(__file__))
    os.makedirs(path, exist_ok=True)
    os.makedirs('{0}/.config/youtube-updater/'.format(home), exist_ok=True)
    path = '{0}/Videos'.format(home)
    channels = '{0}/.config/youtube-updater/channels.txt'.format(home)
    downloaded = '{0}/.config/youtube-updater/downloaded.txt'.format(home)

# We check if we're on windows
if os.name == 'nt':
    windows = True
else:
    windows = False

pid = str(os.getpid())

# If home isn't set then we are likely on windows/ a non-unix like OS
# so we change the /tmp path to the install dir
if windows == True:
    pidfile = "{0}/youtube_updater.pid".format(home)
else:
    pidfile = "/tmp/youtube_updater.pid"


def pid_exists(pid):
    if windows == True:
        print("Running on windows")
        pass
    else:
        try:
            os.kill(int(pid), 0)
            return False
        except OSError:
            return True

# Youtube-dl options

ydl_opts = {
    'format': '22', # This is 720 mp4
    'writedescription': 'True',
    'writethumbnail': 'True',
    'outtmpl': "{0}/%(uploader)s/%(title)s.%(ext)s".format(path),
    'writedescription': 'True',
    'writeinfojson': 'True',
    'writeannotations': 'True',
    'writesub': 'True',
    'allsubs': 'True'

    }

if os.path.isfile(pidfile):
    if pid_exists(open(pidfile).read()) == True:
        print("Found stale lockfile, removing")
        os.unlink(pidfile)
    elif pid_exists(open(pidfile).read()) == False:
        print("{0} already exists, exiting".format(pidfile))
        sys.exit()
    else:
        print('Error writing lockfile')
        sys.exit()

def download(video_title, opts, url):
    if args.l:
        if video_title not in open(args.l).read():
            with open(args.l, mode='a') as f:
                f.write(video_title + '\n')
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([url])
    with open(downloaded, mode='a') as f:
        f.write(url + '\n')


with open(channels) as f:
    youtube_channels = f.read().splitlines()
# We write the pid to file so we can tell if the program is running/has crashed
with open(pidfile, mode='w') as f:
    f.write(str(pid))

for channel in youtube_channels:
    feed = feedparser.parse(channel)
    # This prints the name of the channel
    try:
        print(feed[ "channel" ][ "title" ])
    except KeyError:
        print("Unable to get channel title")
    # The range is the number of videos we check
    for num in range(0,10):
        try:
            url = feed.entries[num].link
            if url not in open(downloaded).read():
                print(url)
                try:
                    download(feed.entries[num].title, ydl_opts, url)
                # This expect is any key error what might be thrown from the video no longer existing
                except KeyError:
                    pass
                except youtube_dl.utils.DownloadError:
                    try:
                        ydl_opts = {
                            'format': 'bestvideo+bestaudio/best',
                            'writedescription': 'True',
                            'writethumbnail': 'True',
                            'outtmpl': "{0}/%(uploader)s/%(title)s.%(ext)s".format(path),
                            'writedescription': 'True',
                            'writeinfojson': 'True',
                            'writeannotations': 'True',
                            'writesub': 'True',
                            'allsubs': 'True'

                            }
                        download(feed.entries[num].title, ydl_opts, url)
                    except youtube_dl.utils.DownloadError:
                        print("Unable to download {0}".format(url))
                        pass
        # We break if the channel has less than 10 videos
        except IndexError:
            break
        else:
            print('Already downloaded')

# We remove the pid file
os.unlink(pidfile)
