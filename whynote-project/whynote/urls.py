from django.urls import path

from . import views

app_name = 'whynote'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:note_id>/', views.detail, name='detail'),
    path('calendar/', views.calendar_button, name='calendar_button')
]
