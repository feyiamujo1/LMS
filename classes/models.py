from django.db import models

# Create your models here.

class Class(models.Model):
    name = models.CharField(max_length=125)
    session = models.CharField(max_length=20)
    created_by = models.ForeignKey('teachers.TeacherProfile', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "classes"
        
    def __str__(self) -> str:
        return f"{self.name}, {self.session}"