#!/usr/bin/env python

import twitter
from config import Config as BaseConfig


class Tweet(object):
    """Twitter Interface."""

    def __init__(self):
        super(Tweet, self).__init__()
        self.config = BaseConfig()
        self.api = twitter.Api(self.config.TWT_CONSUMER_KEY,
                               self.config.TWT_CONSUMER_SECRET,
                               self.config.TWT_ACCESS_TOKEN,
                               self.config.TWT_ACCESS_SECRET)

    def post(self, message):
        print('Posting tweet: ' + message)
        self.api.PostUpdate(message)
