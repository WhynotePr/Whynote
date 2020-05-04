from django.forms import ModelForm, TimeInput, DateInput
from .models import *

class EventForm(ModelForm):
    
    class Meta:
        model = Event
        widgets = {
            'day': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'start_time': TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'end_time': TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['day'].input_formats = ('%Y-%m-%d',)
        self.fields['start_time'].input_formats = ('%H:%M',)
        self.fields['end_time'].input_formats = ('%H:%M',)

class NoteForm(ModelForm):

    class Meta:
        model = Note
        fields = ('note_title', 'note_text')

class TabForm(ModelForm):

    class Meta:
        model = Tabsettings
        fields = ('textcolor', 'bgcolor', 'textstyle', 'fontfamily',
                  'fontsize')

class BookForm(ModelForm):
    """For uploading pdf files"""
    
    class Meta:
        model = Book
        fields = ('title', 'author', 'pdf')


















