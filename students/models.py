from django.db import models
from django.contrib.auth import get_user_model
from .managers import StudentManager
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class Student(User):
    base_role = User.Role.STUDENT
    students = StudentManager()

    class Meta:
        proxy = True

class StudentProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True, upload_to="images/")
    student_id = models.IntegerField(null=True, blank=True)

@receiver(post_save, sender=Student)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "STUDENT":
        StudentProfile.objects.create(user=instance)