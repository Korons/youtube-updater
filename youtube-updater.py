#!/usr/bin/python3

import os
import sys
import feedparser

home = os.getenv("HOME")
path = '{0}/Videos'.format(home)
channels = '{0}/.config/youtube-updater/channels.txt'.format(home)
downloaded = '{0}/.config/youtube-updater/downloaded.txt'.format(home)

pid = str(os.getpid())
pidfile = "/tmp/youtube_updater.pid"

if os.path.isfile(pidfile):
    print ("{0} already exists, exiting".format(pidfile))
    sys.exit()

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
                w_thumb = '--write-thumbnail'
                w_descript = '--write-description'
                # This does a system call for youtube-dl.
                # TODO change from system call to youtube-dl lib
                youtube_dl_call = ('youtube-dl -i -w -o "{0}/%(uploader)s/%(title)s.%(ext)s" "{1}" -f 22 {2} {3} -R 10'.format(path, url, w_thumb, w_descript))
                os.system(youtube_dl_call)
                with open(downloaded, mode='a') as f:
                    f.write(url + '\n')
        # We break if the channel has less than 10 videos
        except IndexError:
            break
        else:
            print('Already downloaded')
# We remove the pid file
os.unlink(pidfile)
