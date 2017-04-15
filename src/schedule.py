import os
import praw
import urllib2
import simplejson as json
import xml.etree.ElementTree as ET
import dateutil.parser
import pytz
import re
from config import Config as BaseConfig
from datetime import datetime, date, time
from xml.dom import minidom

class Schedule(object):
	"""Creates a new White Sox Baseball Schedule"""

	def __init__(self):
		super(Schedule, self).__init__()
		self.TODAY = date.today()
		self.MONTH = datetime.now().strftime("%m")
		self.YEAR = self.TODAY.year
		self.TZ = {'CT':pytz.timezone('US/Central')}
		# API Configuration
		self.config = BaseConfig()
		self.API_URL = 'http://api.sportradar.us/mlb-t5/games/' + str(self.YEAR) + '/REG/schedule.xml?api_key=' + self.config.API_KEY
		self.XML_NS = '{http://feed.elasticstats.com/schema/baseball/v5/schedule.xsd}'
		self.XML_FILE = urllib2.urlopen(self.API_URL)
		self.CWD = os.path.dirname(os.path.realpath(__file__))
		self.TREE = ET.parse(self.XML_FILE)
		self.ROOT = self.TREE.getroot()

	def getSchedule(self):
		s = []
		# Traverse the XML
		for game in self.ROOT.iter(self.XML_NS + 'game'):
			home = game.find(self.XML_NS + 'home')
			away = game.find(self.XML_NS + 'away')
			home_abbr = home.get('abbr')
			away_abbr = away.get('abbr')
			newdate = dateutil.parser.parse(game.get('scheduled'), tzinfos=self.TZ)
			utc_time = newdate.astimezone(pytz.UTC)
			cst_time = utc_time.astimezone(pytz.timezone('US/Central'))
			gamemonth = cst_time.strftime('%m')
			gametime = cst_time.strftime('%m-%d-%y %I:%M')
			network = game.find(self.XML_NS + 'broadcast').get('network')

			if (home_abbr == "CWS" or away_abbr == "CWS") and self.MONTH == gamemonth:

				# Bold the White Sox
				if home_abbr == "CWS":
					home_abbr = "**CWS**"
				if away_abbr == "CWS":
					away_abbr = "**CWS**"

				s.append({
					'home': home_abbr,
					'away': away_abbr,
					'gametime': gametime,
					'network': network
				})

		schedule = sorted(s, key=lambda k: k['gametime'])

		return schedule

	def createTable(self):
		schedule = self.getSchedule()
		table = []
		top_marker = '[//]: # (Begin Schedule)'
		bottom_marker = '[//]: # (End Schedule)'
		# Setup the Reddit Table
		table.append(top_marker)
		table.append(u'###Schedule###\n\n| Home | Away | Time | Network |\n|:-|:-|:-:|:-:|')

		for i in range(len(schedule)):
			table.append('|' + schedule[i]['home'] + '|' + schedule[i]['away'] + '|' + schedule[i]['gametime'] + '|' + schedule[i]['network'] + '|')

		table.append(bottom_marker)

		# encode to utf-8 for reddit tables to format properly
		finalschedule = '\n'.join(table)
		finalschedule.encode(encoding='UTF-8',errors='strict')

		return finalschedule

	def postSchedule(self):

		print 'Beginning schedule update...'

		# Reddit user_agent
		r = praw.Reddit('OAuth Baseball-GDT V. 3.0.1'
                        'ChiSox Posts Gamethreads to r/whitesox')
		r.set_oauth_app_info(client_id=self.config.CLIENT_ID,
							client_secret=self.config.CLIENT_SECRET,
							redirect_uri=self.config.REDIRECT_URI)
		r.refresh_access_information(self.config.REFRESH_TOKEN)

		# Get subreddit settings
		subreddit = r.get_subreddit(self.config.SUBREDDIT)
		settings = subreddit.get_settings()

		# store the old description
		description = settings['description']

		# Get the new schedule
		new_schedule = self.createTable()

		# Replace the old standings
		new_description = re.sub('(\[\/\/\]: # \((Begin Schedule)\))([^"]*)(\[\/\/\]: # \((End Schedule)\))', new_schedule, description)

		new_description.encode(encoding='UTF-8',errors='strict');

		# Update Description
		subreddit.update_settings(description=new_description)

		print("Schedule updated...")

	def run(self):
		self.config.checkAuthSettings()
		self.postSchedule()


s = Schedule()
s.run()
