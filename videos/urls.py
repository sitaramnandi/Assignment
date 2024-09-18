from django.urls import path
from django.contrib import admin
from videos import views
urlpatterns = [
    path('admin/', admin.site.urls),
   path("video_upload/",views.video_upload),
   path("video_list/",views.video_list,name="video_list"),
   path("subtitles_search/<int:video_id>/",views.subtitles_search,name="search_subtitle"),
]