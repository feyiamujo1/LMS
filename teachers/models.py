from django.db import models
from django.contrib.auth import get_user_model
from .managers import TeacherManager
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

User = get_user_model()

class Teacher(User):
    base_role = User.Role.STAFF
    teachers = TeacherManager()

    class Meta:
        proxy = True

class TeacherProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True, upload_to="images/")
    teacher_id = models.IntegerField(null=True, blank=True)

@receiver(post_save, sender=Teacher)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "STAFF":
        TeacherProfile.objects.create(user=instance)