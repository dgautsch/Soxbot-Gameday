#!/usr/bin/env python

import os
import simplejson as json
class Config(object):
    """Environment Configuration."""
    def __init__(self):
        super(Config, self).__init__()
        self.CWD = os.path.dirname(os.path.realpath(__file__))
        self.CLIENT_ID = os.environ.get('CLIENT_ID')
        self.CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
        self.REFRESH_TOKEN = os.environ.get('REFRESH_TOKEN')
        self.SUBREDDIT = os.environ.get('SUBREDDIT')
        self.API_KEY = os.environ.get('SPORT_RADAR_KEY')
        self.TWT_CONSUMER_KEY = os.environ.get('TWT_CONSUMER_KEY')
        self.TWT_CONSUMER_SECRET = os.environ.get('TWT_CONSUMER_SECRET')
        self.TWT_ACCESS_TOKEN = os.environ.get('TWT_ACCESS_TOKEN')
        self.TWT_ACCESS_SECRET = os.environ.get('TWT_ACCESS_SECRET')
        with open(self.CWD + '/settings.json') as data:
			settings = json.load(data)
			self.REDIRECT_URI = settings.get('REDIRECT_URI')

    def checkAuthSettings(self):
        if self.CLIENT_ID == None: return "Missing CLIENT_ID"
        if self.CLIENT_SECRET == None: return "Missing CLIENT_SECRET"
        if self.REDIRECT_URI == None: return "Missing REDIRECT_URI"
        if self.REFRESH_TOKEN == None: return "Missing REFRESH_TOKEN"
        if self.SUBREDDIT == None: return "Missing SUBREDDIT"
        if self.TWT_CONSUMER_KEY == None: return "Missing TWT_CONSUMER_KEY"
        if self.TWT_CONSUMER_SECRET == None: return "Missing TWT_CONSUMER_SECRET"
        if self.TWT_ACCESS_TOKEN == None: return "Missing TWT_ACCESS_TOKEN"
        if self.TWT_ACCESS_SECRET == None: return "Missing TWT_ACCESS_SECRET"
