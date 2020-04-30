from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy

from django.views.generic.list import ListView
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime
from django.utils import timezone
import calendar

from django.core.files.storage import FileSystemStorage

from .models import *
from .utils import Calendar
from .forms import *


bgcolor = "#E8E8E8"
textcolor = "black"
textstyle = "normal"
fontfamily = "Montserrat"
fontsize = 14

def home(request, bgcol="#E8E8E8",
         textcol="black",
         textst="normal",
         textsi = "14"):
    latest_notes_list = Note.objects.order_by('-public_date')
    bgcolor = bgcol
    textcolor = textcol
    textstyle = textst
    textsize = textsi
    return render(request, 'home.html', {'latest_notes': latest_notes_list,
                                         'bgcolor': bgcol,
                                         'textcolor': textcol,
                                         'textstyle': textst,
                                         'fontfamily': fontfamily,
                                         'textsize': textsize})

def detail(request, note_id):
    try:
        nt = Note.objects.get(id = note_id)
    except:
        raise Http404("The note is not found")
    return render(request, 'innote.html', {"note": nt})


# For calendar

def calendar_button(request):
    return render(request, 'calendar.html')

class CalendarView(ListView):
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))
        # Instantiate calendar class with today's year and date
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('whynote:calendar'))
    return render(request, 'event.html', {'form': form})


def add_note_button(request):
    return render(request, 'add_note.html')

def post_new(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.public_date = timezone.now()
            post.save()
            return redirect('whynote:detail', note_id=post.pk)
    else:
        form = NoteForm()
    return render(request, 'add_note.html', {'form': form})

# предпологается для осуществления папок, name - имя папки
def folder(request, name):
    return render(request, 'folders.html', name)

def tab_set(request):
    if request.method != "POST":
        return render(request,'text_and_background_settings.html',
                      {'form': TabForm(request.POST)})
    else:
        form = TabForm(request.POST)
        global bgcolor,textcolor,textstyle,fontsize
        tabset = form.save(commit=False)
        bgcolor = tabset.bgcolor
        textcolor = tabset.textcolor
        textstyle = tabset.textstyle
        fontfamily = tabset.fontfamily
        fontsize = tabset.fontsize
        return render(request, 'home.html',
                      {'latest_notes': Note.objects.order_by('note_title'),
                       'bgcolor': bgcolor,
                       'textcolor': textcolor,
                       'fontfamily': fontfamily,
                       'fontsize': fontsize})

# For uploading files
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)


def book_list(request):
    return render(request, 'book_list.html')

def upload_book(request):
    form = BookForm()
    return render(request, 'upload_book.html', {'form': form})
    


















