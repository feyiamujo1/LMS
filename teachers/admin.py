from django.contrib import admin
from .models import Teacher, TeacherProfile, ClassTeacher
# Register your models here.

admin.site.register(Teacher)
admin.site.register(TeacherProfile)
admin.site.register(ClassTeacher)