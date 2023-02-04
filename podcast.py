#! /usr/bin/env python3
from pyPodcastParser.Podcast import Podcast as pyPodcast
import requests
import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class Podcast:
    def __init__(self, url):
        self.url = url  # feed url of podcast 
        self.__fetchFeed() # fetch feed
        self.title = self.__getTitle() # title of podcast
        self.epList = [] # a list of all episodes
        self.refreshFeed() # reads feed and populates the episode list

    def __fetchFeed(self):
        try:
            r = requests.get(self.url)
            self.feed_content = r.content
        except Exception as e:
            log.error(f'failed to download feed from URL: %s Error: %e', self.url, e)

    def __getTitle(self):
    # extract title of podcast from feed
        try:
            p = pyPodcast(self.feed_content)
            return p.title
        except Exception as e:
            log.error(f'failed reading podcast name: %e', e)
            return ""

    def refreshFeed(self):
    # reads feed and populates the episode list
        try:
            p = pyPodcast(self.feed_content)
            for i in p.items:
                _t = i.title
                _url = i.enclosure_url
                _pd = i.published_date 
                _dur = i.itunes_duration
                _guid = i.guid
                eObj = Episode(self.title, _t, _url, _pd, _dur, _guid)
                self.epList.append(eObj)
            log.info(f'%s: feed refreshed, %s episodes found.', self.title, len(items) )
        except Exception as e:
            log.error(f'%s: feed scraping failed: %s', self.title, e)

class Episode:
    def __init__(self, podcast, title, url, date, durationStr, guid):
        self.podcast = podcast          # Podcast Title this episode belongs to 
        self.title = title              # title
        self.date = date                # date when published (string)
        self.url = url                  # url of audio file
        self.guid = guid                # GUID
        self.fname = ""                 # filename for disk storage
        self.fpath = ""                 # path for disk storage
        self.durationStr = durationStr  # duration string as in feed
        self.durationSec = self.__durStr2sec(durationStr) # ... in sec

    def __durStr2sec(self, str):
        h, m, s = str.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)