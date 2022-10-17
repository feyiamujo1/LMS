from django.db import models
from teachers.models import TeacherProfile
from students.models import StudentProfile

# Create your models here.

class Class(models.Model):
    name = models.CharField(max_length=125)
    session = models.CharField(max_length=20)
    students = models.ManyToManyField(StudentProfile)
    teachers = models.ManyToManyField(TeacherProfile)

    def __str__(self) -> str:
        return f"{self.name}, {self.session}"