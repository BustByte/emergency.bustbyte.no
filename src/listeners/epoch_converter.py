import pytz
import time
from datetime import datetime

class EpochConverter:

    timezone = pytz.timezone('Europe/Oslo')
    date_format = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def to_date_string(epoch):
        try:
            epoch = int(epoch) / 1000
        except ValueError:
            raise ValueError('Invalid epoch: ' + epoch)

        dt = datetime.fromtimestamp(epoch, EpochConverter.timezone)
        return dt.strftime(EpochConverter.date_format)
