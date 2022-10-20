from django.db import models
from teachers.models import TeacherProfile
from classes.models import Class
# Create your models here.


class Announcement(models.Model):
    posted_by = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    posted_to = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, null=True, blank=True)
    body = models.TextField(max_length=300)
    attachment = models.FileField(max_length=20000, upload_to="files/")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "<Announcement %r>" % self.title