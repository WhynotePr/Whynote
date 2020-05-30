#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin
from .models import Note, Comment, Event

admin.site.register(Note)
admin.site.register(Comment)
admin.site.register(Event)
