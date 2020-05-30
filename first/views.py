from django.shortcuts import render
from first.forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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


def index(request):
    return redirect('first:home')

@login_required
def special(request):
    return HttpResponse("You are logged in!")

@login_required
def user_logout(request):
    logout(request)
    userlogin = ""
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'registration.html',
                          {'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        global userlogin
        userlogin = username
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})


#------------------------------------------------------------------------
userlogin = ""

def home(request):
    lnl = list()
    for obj in Note.objects.all().order_by('-public_date'):
    	if obj.username == userlogin:
    		lnl.append(obj)
    return render(request, 'home.html', {'latest_notes': lnl})

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
        cal = Calendar(d.year, d.month, userlogin)
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
    if 'create_event' in request.POST and form.is_valid():
        post = form.save(commit=False)
        post.public_date = timezone.now()
        global userlogin
        post.username = userlogin
        post.save()
        return HttpResponseRedirect(reverse('first:calendar'))
    if 'delete_event' in request.POST and event_id:
        event = Event.objects.get(pk=event_id)
        event.delete()
        return HttpResponseRedirect(reverse('first:calendar'))
    return render(request, 'event.html', {'form': form})

def add_note_button(request):
    return render(request, 'add_note.html')

def post_new(request, username="thisuserwillneverbehere"):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.public_date = timezone.now()
            global userlogin
            post.username = userlogin
            post.save()
            return redirect('first:detail', note_id=post.pk)
    else:
        form = NoteForm()
    userlogin = username
    return render(request, 'add_note.html', {'form': form})

# предпологается для осуществления папок, name - имя папки
def folder(request, name):
    return render(request, 'folders.html', name)

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
    books = []
    for obj in Book.objects.all():
        if obj.username == userlogin:
            books.append(obj)
    return render(request, 'book_list.html', {'books': books})

def upload_book(request, username="thisuserwillneverbehere"):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            global userlogin
            post.username = userlogin
            post.save()
            return redirect('first:book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {'form': form})

def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('first:book_list')
