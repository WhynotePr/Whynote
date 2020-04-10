from django.urls import path

from . import views

app_name = 'whynote'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:note_id>/', views.detail, name='detail'),
    path('calendar/', views.calendar_button, name='calendar_button'),
    path('add_note/',views.add_note_button, name = 'add_note_button'),
    path('post/new/', views.post_new, name='post_new'),
    path('folders/', views.folder, name= "folder"),
    path('tab_settings/', views.tab_set, name = "tab_set")
]
