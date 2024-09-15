from datetime import datetime, timedelta

def utime(sub_period):
    now = datetime.utcnow()
    if sub_period == 'm': 
        time = now + timedelta(days=30)
    elif sub_period == '6m':
        time = now + timedelta(days=180)
    elif sub_period == 'y':
        time = now + timedelta(days=365)
    elif sub_period == 'lt':
        time = now + timedelta(days=36500)
    return int(time.timestamp()*1000)
