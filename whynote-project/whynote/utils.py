from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event
from django.utils import timezone

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()
    
    def formatday(self, day, events):
        events_per_day = events.filter(day__day=day)
        d = '<ol class="list-numbered">'
        for event in events_per_day:
            d += f'<li> {event.get_html_url} </li>'
        d += "</ol>"
        if (day == timezone.now().day
            and self.month == timezone.now().month
            and self.year == timezone.now().year):
            td = f'<td class="active">'
        else:
            td = f'<td>'
        if day != 0:
            return td + f'<div class="card"><div class="card-header '\
                   f'border-dark text-right">'\
                   f'{day}</div><div class="card-body">'\
                   f'<ul class="list-group list-group-flush">'\
                   f'{d}</ul></div></div></td>'
        return '<td></td>'
    
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'
        
    def formatmonth(self, withyear=True):
        events = Event.objects.filter(day__year=self.year,
                                      day__month=self.month)
        cal = f'<table class="table table-bordered" id="calendar">'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)} '
        cal += f'{self.formatweekheader()}'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)} '
        cal += f'</table>'
        return cal
