import tweet

class Program(object):
    """Twitter Interface."""

    def __init__(self):
        super(Program, self).__init__()

    def run(self):
        t = tweet.Tweet()
        t.post('hi')

s = Program()
s.run()
