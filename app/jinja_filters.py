__author__ = 'mehanig'
from datetime import datetime


def format_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="EE dd.MM.y HH:mm"
    return datetime.utcfromtimestamp(value)

def status_info(value):
    if int(value):
        return 'Finished'
    else:
        return 'Not done yet'