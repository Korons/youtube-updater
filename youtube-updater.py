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

def pid_exists(pid):
    try:
        os.kill(int(pid), 0)
        return False
    except OSError:
        return True

# Youtube-dl options

ydl_opts = {
    'format':'22',
    'writedescription':'True',
    'writethumbnail':'True',
    'outtmpl':"{0}/%(uploader)s/%(title)s.%(ext)s".format(path),
    'writedescription':'True',
    'writeinfojson':'True',
    'writeannotations':'True',
    'writesub':'True'

    }

if os.path.isfile(pidfile):
    if pid_exists(open(pidfile).read()) == True:
        print("Found stale lockfile, removing")
        os.unlink(pidfile)
    elif pid_exists(open(pidfile).read()) == False:
        print ("{0} already exists, exiting".format(pidfile))
        sys.exit()
    else:
        print('Something went wrong')
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
                print (url)
                try:
                    download(ydl_opts, url)
                # This expect is any key error what might be thrown from the video no longer existing
                except KeyError:
                    pass
                except youtube_dl.utils.DownloadError:
                    try:
                        ydl_opts = {
                            'format': 'bestvideo+bestaudio/best',
                            'writedescription':'True',
                            'writethumbnail':'True',
                            'outtmpl':"{0}/%(uploader)s/%(title)s.%(ext)s".format(path),
                            'writedescription':'True',
                            'writeinfojson':'True',
                            'writeannotations':'True',
                            'writesub':'True'
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
