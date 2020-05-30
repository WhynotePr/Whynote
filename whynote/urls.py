from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'whynote'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:note_id>/', views.detail, name='detail'),
    path('add_note/',views.add_note_button, name = 'add_note_button'),
    path('post/new/', views.post_new, name='post_new'),
    
    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    path('calendar/', views.calendar_button, name='calendar_button'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    
    path('folders/', views.folder, name='folder'),
    
    path('tab_settings/', views.tab_set, name='tab_set'),
    
    path('upload/', views.upload, name='upload'),
    path('books/', views.book_list, name='book_list'),
    path('books/upload/', views.upload_book, name='upload_book'),
    path('books/<int:pk>/', views.delete_book, name='delete_book')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

