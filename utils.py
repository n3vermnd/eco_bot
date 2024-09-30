import datetime

def utime(sub_period):
    periods = {
        'm': 30,
        '6m': 180,
        'y': 365,
        'lt': 36500
    }
    days = periods.get(sub_period)
    return int((datetime.datetime.now() + datetime.timedelta(days=days)).timestamp() * 1000)