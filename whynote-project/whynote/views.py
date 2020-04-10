from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Note, Comment, Tabsettings
from .forms import NoteForm, TabForm
from django.utils import timezone

bgcolor = "white"
textcolor = "black"
textstyle = "normal"
fontfamily = "Montserrat"
fontsize = 14
def home(request,bgcol = "000000" ,textcol = "blue", textst = "normal", textsi = "14"):
    latest_notes_list = Note.objects.order_by('note_title')
    bgcolor = bgcol
    textcolor = textcol
    textstyle = textst
    textsize = textsi
    return render(request, 'home.html', {'latest_notes': latest_notes_list,'bgcolor': bgcol,'textcolor':textcol,'textstyle':textst,'fontfamily':fontfamily, 'textsize':textsize})

def detail(request, note_id):
    try:
        nt = Note.objects.get(id = note_id)
    except:
        raise Http404("The note is not found")
    return render(request, 'innote.html', {"note": nt,"textcolor":textcolor,"bgcolor":bgcolor,"textstyle":textstyle,'fontfamily':fontfamily,'fontsize':fontsize})

def calendar_button(request):
    return render(request, 'calendar.html')

def add_note_button(request):
	return render(request,'add_note.html')

def post_new(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.public_date = timezone.now()
            post.save()
            return redirect('whynote:detail', note_id = post.pk)
    else:
        form = NoteForm()
    return render(request, 'add_note.html', {'form': form})

# предпологается для осуществления папок, name - имя папки
def folder(request,name):
	return render(request,'folders.html', name)
def tab_set(request):
	if request.method != "POST":
		return render(request,'text_and_background_settings.html', {'form':TabForm(request.POST)})
	else:
		form = TabForm(request.POST)
		global bgcolor,textcolor,textstyle,fontsize
		tabset = form.save(commit = False)
		bgcolor = tabset.bgcolor
		textcolor = tabset.textcolor
		textstyle = tabset.textstyle
		fontfamily = tabset.fontfamily
		fontsize = tabset.fontsize
		return render(request,'home.html', {'latest_notes': Note.objects.order_by('note_title'),'bgcolor': bgcolor,'textcolor':textcolor,'fontfamily':fontfamily,'fontsize':fontsize})



