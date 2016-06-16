#!/usr/bin/python3

import os
import sys
import feedparser
import youtube_dl

home = os.getenv("HOME")
path = '{0}/Videos'.format(home)
channels = '{0}/.config/youtube-updater/channels.txt'.format(home)
downloaded = '{0}/.config/youtube-updater/downloaded.txt'.format(home)

pid = str(os.getpid())
pidfile = "/tmp/youtube_updater.pid"

# Youtube-dl options

ydl_opts = {
    'format':'22',
    'writedescription':'True',
    'writethumbnail':'True',
    'outtmpl':"{0}/%(uploader)s/%(title)s.%(ext)s".format(path)
    }

if os.path.isfile(pidfile):
    print ("{0} already exists, exiting".format(pidfile))
    sys.exit()

def download(opts, url):
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
    print (feed[ "channel" ][ "title" ])
    # The range is the number of videos we check
    for num in range(0,10):
        try:
            url = feed.entries[num].link
            if url not in open(downloaded).read():
                # This does a system call for youtube-dl.
                print (url)
                try:
                    download(ydl_opts, url)
                # This expect is here to catch any format errors from youtube
                except KeyError:
                    pass
                except youtube_dl.utils.DownloadError:
                    try:
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'writedescription':'True',
                            'writethumbnail':'True',
                            'outtmpl':"{0}/%(uploader)s/%(title)s.%(ext)s".format(path)
                            }
                        download(ydl_opts, url)
                    except youtube_dl.utils.DownloadError:
                        pass
        # We break if the channel has less than 10 videos
        except IndexError:
            break
        else:
            print('Already downloaded')

# We remove the pid file
os.unlink(pidfile)
