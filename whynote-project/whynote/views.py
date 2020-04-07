from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Note, Comment


def home(request):
    latest_notes_list = Note.objects.order_by('note_title')
    return render(request, 'home.html', {'latest_notes': latest_notes_list})

def detail(request, note_id):
    try:
        nt = Note.objects.get(id = note_id)
    except:
        raise Http404("The note is not found")
    return render(request, 'innote.html', {"note": nt})

def calendar_button(request):
    return render(request, 'calendar.html')
