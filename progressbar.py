import sys


class Counter:
    def __init__(self, message=''):
        self.message = message
        self.index = 0

    def update(self):
        sys.stdout.write('%s\r' % (self.message + ' ' + str(self.index)))
        sys.stdout.flush()

    def finish(self):
        print('\n')


class Bar:
    def __init__(self, message='', max=100, bar_len=20):
        self.message = message
        self.max = max
        self.count = 0
        self.bar_len = bar_len

    def next(self, increment=1):
        self.count += increment
        filled_len = int(round(self.bar_len * self.count / float(self.max)))

        percents = str(round(100.0 * self.count / float(self.max), 1)) + '%'
        if len(percents) < 6:
            percents = percents + ' ' * (6 - len(percents))
        ratio = str(self.count) + '/' + str(self.max)
        bar = '█' * filled_len + '░' * (self.bar_len - filled_len)

        sys.stdout.write('%s |%s| %s %s\r' % (percents, bar, self.message, ratio))
        sys.stdout.flush()

    def finish(self):
        print()
