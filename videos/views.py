from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from videos.models import Video
from .forms import VideoForm
from .tasks import process_video
def video_upload(request):
    if request.method=="POST":
        form=VideoForm(request.POST,request.FILES)
        if form.is_valid():
            video=form.save()
            process_video.delay(video.id)
            return redirect("video_list")
    else:
        form=VideoForm()
    return render(request,"video/upload_video.html",{"form":form})

def video_list(request):
    video=Video.objects.all()
    return render(request,"video/video_list.html",{"videos":video})


def subtitles_search(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    query = request.GET.get("q", "")
    subtitles = video.subtitles.filter(content__icontains=query)
    return render(request, 'video/search.html', {'subtitles': subtitles, 'video': video})
