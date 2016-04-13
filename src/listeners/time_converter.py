import pytz
import time
from datetime import datetime

class TimeConverter:

    timezone = pytz.timezone('Europe/Oslo')
    date_format = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def epoch_to_date_string(epoch):
        try:
            epoch = int(epoch) / 1000
        except ValueError:
            raise ValueError('Invalid epoch: ' + epoch)

        dt = datetime.fromtimestamp(epoch, TimeConverter.timezone)
        return dt.strftime(TimeConverter.date_format)

    @staticmethod
    def twitter_time_to_date_string(twitter_time):
        try:
            dt = datetime.strptime(twitter_time, '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.utc)
            dt = dt.astimezone(TimeConverter.timezone)
        except ValueError:
            raise ValueError('Invalid twitter time: ' + twitter_time)
        return dt.strftime(TimeConverter.date_format)
