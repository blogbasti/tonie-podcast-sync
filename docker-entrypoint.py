import os
import sys
from toniepodcastsync import ToniePodcastSync, Podcast
from bs4 import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

import argparse

parser = argparse.ArgumentParser(description='Sync podcast to creative tonie.')
parser.add_argument('--tonie-id',
                    required=True, 
                    help='creative tonie id to upload latest episodes of podcast to')
parser.add_argument('--podcast-feed-url',
                    required=True,
                    help='Podcast feed URL')
parser.add_argument('--username',
                    required=False,
                    help='Tonie Cloud username')
parser.add_argument('--password',
                    required=False,
                    help='Tonie Cloud password')

args = parser.parse_args()


def getValueFromCmdlineOrEnvironment(cmdline_var, cmdline_name, env_var_name):
    var = None

    if ( None != os.getenv(env_var_name) ):
        var = os.getenv(env_var_name)

    if ( None != cmdline_var ):
        var = cmdline_var

    if ( None == var ):
        print(
            "%s or environment variable %s is required!" % (
                cmdline_name,
                env_var_name
            ),
            file=sys.stderr
        )
        exit(1)

    return var

username = getValueFromCmdlineOrEnvironment(
    cmdline_var=args.username,
    cmdline_name='--username',
    env_var_name='TONIE_CLOUD_USERNAME'
)

password = getValueFromCmdlineOrEnvironment(
    cmdline_var=args.password,
    cmdline_name='--password',
    env_var_name='TONIE_CLOUD_PASSWORD'
)

# create two Podcast objects, providing the feed URL to each
# pumuckl = Podcast("https://feeds.br.de/pumuckl/feed.xml")
# maus = Podcast("https://kinder.wdr.de/radio/diemaus/audio/gute-nacht-mit-der-maus/diemaus-gute-nacht-104.podcast")
# diemausMusik = Podcast("https://kinder.wdr.de/radio/diemaus/audio/diemaus-musik/diemaus-musik-106.podcast")
p = Podcast(args.podcast_feed_url)

# create instance of ToniePodcastSync
tps = ToniePodcastSync(username, password)

# for an overview of your creative tonies and their IDs
tps.printToniesOverview()

# sync newest episode to tonie
tps.syncPodcast2Tonie(p, args.tonie_id)