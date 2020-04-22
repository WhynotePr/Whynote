from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'whynote'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:note_id>/', views.detail, name='detail'),
    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    path('calendar/', views.calendar_button, name='calendar_button'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    path('add_note/',views.add_note_button, name = 'add_note_button'),
    path('post/new/', views.post_new, name='post_new'),
    path('folders/', views.folder, name= "folder"),
    path('tab_settings/', views.tab_set, name = "tab_set"),
]
