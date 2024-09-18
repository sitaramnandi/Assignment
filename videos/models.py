from django.db import models

# Create your models here.
class Video(models.Model):
    title=models.CharField(max_length=255)
    video_file=models.FileField(upload_to="videos/")
    uploaded_at=models.DateTimeField(auto_now_add=True,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.title
    
class Subtitle(models.Model):
    video=models.ForeignKey(Video,related_name="subtitles",on_delete=models.CASCADE)
    language=models.CharField(max_length=255)
    content=models.TextField()
    timestamp=models.CharField(max_length=50)

    def __str__(self):
        return f"{self.video.title} - {self.language}"