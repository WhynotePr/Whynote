from django import forms
from first.models import *
from django.forms import ModelForm, TimeInput, DateInput
from django.contrib.auth.models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'email', 'password')
        
class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = UserProfileInfo
         fields = ('portfolio_site','profile_pic')

class EventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        widgets = {
            'day': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'start_time': TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'end_time': TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            }
        fields = ('eventtitle', 'day', 'start_time', 'end_time', 'notes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['day'].input_formats = ('%Y-%m-%d',)
        self.fields['start_time'].input_formats = ('%H:%M',)
        self.fields['end_time'].input_formats = ('%H:%M',)
        self.fields['notes'].required = False

class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ('note_title', 'note_text')


class BookForm(forms.ModelForm):
    """For uploading pdf files"""
    
    class Meta:
        model = Book
        fields = ('title', 'author', 'pdf', 'cover')
