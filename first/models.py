from django.contrib.auth.models import User

from django.db import models
import datetime
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    def __str__(self):
        return self.user.username

class Note(models.Model):
    note_title = models.CharField('the title of a note',
                                  max_length = 200)
    note_text = models.TextField()
    public_date = models.DateTimeField('The publication date',
                                       default=timezone.now())
    username = models.CharField('user name', max_length = 300)

    def __str__(self):
        return self.note_title

    def preview(self):
        return self.note_text[:120]
    
class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete = models.CASCADE)
    author_name = models.CharField('The author\'s name', max_length=70)
    comment_text = models.CharField('The text of a comment', max_length=200)

    def __str__(self):
        return self.author_name

class Event(models.Model):
    eventtitle = models.CharField('The title of your event',
                                  default = 'New event',
                                  max_length=200)
    day = models.DateField('Day of the event', default=timezone.now(),
                           help_text='Use the following format: YYYY-MM-DD')
    start_time = models.TimeField('Starting time', help_text='Starting time')
    end_time = models.TimeField('Final time', help_text='Final time')
    notes = models.TextField('Textual notes', help_text='Textual notes')
    username = models.CharField('user name', max_length = 300) 

    def __str__(self):
        return self.eventtitle
    
    @property
    def get_html_url(self):
        url = reverse('first:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.eventtitle} </a>'
    
    class Meta:
        verbose_name = 'Scheduling'
        verbose_name_plural = 'Scheduling'

    def check_overlap(self, fixed_id, fixed_start, fixed_end,
                      new_id, new_start, new_end)->bool:
        """Return True if there are collisions of two events"""
        if new_start == fixed_end or new_end == fixed_start:
            return False
        if new_id == fixed_id:
            return False
        #If the start or the end is between fixed boundaries
        is_start_in = new_start >= fixed_start and new_start <= fixed_end
        is_end_in = new_end >= fixed_start and new_end <= fixed_end
        if is_start_in or is_end_in:
            return True
        #If the new event is inside the fixed
        if new_start <= fixed_start and new_end >= fixed_end:
            return True
    
    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Ending time must be after starting time')
        #Sort events by day
        events = Event.objects.filter(day=self.day)
        if events.exists():
            for event in events:
                if self.check_overlap(event.id, event.start_time, event.end_time,
                                      self.id, self.start_time, self.end_time):
                    raise ValidationError(
                        'There is an overlap with another event: '
                        + str(event.day) + ', ' + str(event.start_time)
                        + '-' + str(event.end_time))

class Book(models.Model):
    """Class for uploading files"""
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    #upload_to is a way of setting the upload directory and file name
    pdf = models.FileField('File', upload_to='pdfs/')
    cover = models.ImageField(upload_to='pdfs/covers/', null=True, blank = True)
    
    username = models.CharField('user name', max_length = 300)

    def __str__(self):
        return self.title







