"""docstring for schedulecalendar."""
import calendar
import urllib2
from datetime import datetime, date


class ScheduleCalendar(object):
    """docstring for ScheduleCalendar."""

    def __init__(self):
        super(ScheduleCalendar, self).__init__()
        self.today = date.today()
        self.month = self.today.month
        self.year = self.today.year
        self.strmonth = datetime.now().strftime("%B")
        self.calendar = calendar

    def get_schedule(self, month, year, url):
        """Makes call for the schedule."""

    def build_calendar(self):
        """Builds the calendar for the schedule."""
        self.calendar.setfirstweekday(calendar.SUNDAY)
        standings = []
        standings.append('[//]: # (Begin Schedule)\n')
        standings.append('### Schedule for {month} ###\n'.format(month=self.strmonth))
        standings.append("| S | M | T | W | T | F | S |\n|:-:|:-:|:-:|:-:|:-:|:-:|:-:|\n")
        cell_home_template = "**^{day} []({subreddit})**"
        cell_away_template = "*^{day} []({subreddit})*"
        monthrange = self.calendar.monthcalendar(self.year, self.month)
        for week in monthrange:
            for (i, day) in enumerate(week):
                if i == 0:
                    standings.append('|' + cell_home_template.format(day=day, subreddit='/r/whitesox#') + '|')
                elif i == 6:
                    standings.append(cell_away_template.format(day=day, subreddit='/r/whitesox') + '|\n')
                else:
                    standings.append(cell_away_template.format(day=day, subreddit='/r/whitesox') + '|')
        standings.append('[//]: # (End Schedule)\n')
        print ''.join(standings)

    def run(self):
        """Runs the application"""
        self.build_calendar()

S = ScheduleCalendar()
S.run()
