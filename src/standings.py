import os
import praw
import urllib2
import re
from config import Config as BaseConfig
from time import gmtime, strftime
from datetime import date
from xml.dom import minidom


class Standings(object):
    """Creates a new White Sox Baseball Standings"""

    def __init__(self):
        super(Standings, self).__init__()
        self.config = BaseConfig()
        # API Data
        self.YEAR = date.today().year
        self.API_URL = 'http://api.sportradar.us/mlb-t5/seasontd/' + \
            str(self.YEAR) + '/REG/standings.xml?api_key=' + self.config.API_KEY
        self.XML_NS = 'http://feed.elasticstats.com/schema/baseball/v5/mlb/standings.xsd'

    # helper function to help calculate the win percentage
    def percentage(self, part, whole):
        if whole == 0:
            return 0
        return 100 * float(part) / float(whole)

    # this pulls the standings and fomats them
    def getStandings(self):

        # create an array for our standings
        standings = []

        dom = minidom.parse(urllib2.urlopen(self.API_URL))

        # loop through the xml results appending each row
        for node in dom.getElementsByTagNameNS(self.XML_NS, 'team'):
            standings.append({
                'teamname': node.getAttribute('name'),
                'division': node.parentNode.parentNode.getAttribute('alias') + node.parentNode.getAttribute('alias'),
                'wins': node.getAttribute('win'),
                'losses': node.getAttribute('loss'),
                'gamesback': node.getAttribute('games_back'),
                'streak': node.getAttribute('streak'),
                'l10': node.getAttribute('last_10_won') + '-' + node.getAttribute('last_10_lost'),
                'percentage': self.percentage(int(node.getAttribute('win')), int(node.getAttribute('win')) + int(node.getAttribute('loss')))
            })

        # sort the standings
        n = sorted(standings, key=lambda k: k['division'])
        standings = sorted(n, key=lambda q: q['percentage'], reverse=True)

        return standings

    def createTable(self):

        # create our standings
        standings = self.getStandings()
        tablerows = []
        headerrows = []
        alcrows = []

        # Setup the Reddit Table
        headerrows.append('[//]: # (Begin Standings)')
        headerrows.append('###Standings###\n\n| Team | W | L | GB | S | L10 |\n|:-|:-:|:-:|:-:|:-:|:-:|')

        # Print Each Team's Information
        for i in range(len(standings)):
            # sort by league and division
            if standings[i]['division'] == 'ALC':
                alcrows.append('|' + standings[i]['teamname'] + '|' + standings[i]['wins'] + '|' + standings[i]['losses'] +
                               '|' + standings[i]['gamesback'] + '|' + standings[i]['streak'] + '|' + standings[i]['l10'] + '|')

        # combine all of our lists
        tablerows = headerrows + alcrows

        # add the footer
        dayupdated = strftime("%a, %d %b %Y %X", gmtime())
        tablerows.append('\nThese standings were updated by [u/chisoxbot](http://www.reddit.com/u/chisoxbot) a reddit bot. Standings were last updated on ' + dayupdated)
        tablerows.append('[//]: # (End Standings)')
        finalstandings = '\n'.join(tablerows)

        return finalstandings

    def postStandings(self):

        print 'Beginning standings update for r/' + self.config.SUBREDDIT + '...'

        # Reddit user_agent
        r = praw.Reddit(client_id=self.config.CLIENT_ID,
                        client_secret=self.config.CLIENT_SECRET,
                        redirect_uri=self.config.REDIRECT_URI,
                        refresh_token=self.config.REFRESH_TOKEN,
                        user_agent='python:chisoxbot:v1.0.0 (by /u/logicalriot)')
        # Get subreddit settings
        subreddit = r.subreddit(self.config.SUBREDDIT)
        mod = subreddit.mod
        settings = mod.settings()

        # store the old description
        description = settings['description']

        # Get the new schedule
        new_standings = self.createTable()

        # Replace the old standings
        new_description = re.sub('(\[\/\/\]: # \((Begin Standings)\))([^"]*)(\[\/\/\]: # \((End Standings)\))', new_standings, description)

        new_description.encode(encoding='UTF-8', errors='strict')

        # Update Description
        mod.update(description=new_description)

        print 'Standings updated...'

    def run(self):
        self.config.checkAuthSettings()
        self.postStandings()


s = Standings()
s.run()
