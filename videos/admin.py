from django.contrib import admin
from .models import Video,Subtitle
# Register your models here.

class Videoadmin(admin.ModelAdmin):
    list_display=fields = ['title', 'video_file'] 

class SubtitleAdmin(admin.ModelAdmin):
    list_display=["content","language"]

admin.site.register(Video,Videoadmin)
admin.site.register(Subtitle,SubtitleAdmin)
