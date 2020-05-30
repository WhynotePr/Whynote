from django.conf.urls import url
from django.urls import path
from django.conf import settings
from first import views
from django.conf.urls.static import static
# SET THE NAMESPACE!
app_name = 'first'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    path('', views.home, name='home'),
    path('<int:note_id>/', views.detail, name='detail'),
    path('add_note/',views.add_note_button, name = 'add_note_button'),
    path('post/new/<username>/', views.post_new, name='post_new'),
    
    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    path('calendar/', views.calendar_button, name='calendar_button'),
    url(r'^event/new/$', views.event, name='event_new'),
    url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
    
    path('folders/', views.folder, name='folder'),
    
    path('upload/', views.upload, name='upload'),
    path('files/', views.book_list, name='book_list'),
    path('files/upload/', views.upload_book, name='upload_book'),
    path('files/<int:pk>/', views.delete_book, name='delete_book')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
