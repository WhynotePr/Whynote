from django import forms

from .models import Note,Tabsettings

class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ('note_title','note_text')

class TabForm(forms.ModelForm):

	class Meta:
		model = Tabsettings
		fields = ('textcolor','bgcolor','textstyle',"fontfamily",'fontsize')

