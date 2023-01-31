from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from announcements.models import Announcement, Lesson
from students.models import StudentProfile
from teachers.models import TeacherProfile

from announcements.serializers import AnnouncementListCreateSerializer, LessonListCreateSerializer
# Create your views here.

class AnnouncementListCreateView(ListCreateAPIView):
    serializer_class = AnnouncementListCreateSerializer
    queryset = Announcement.objects.all()

    def get_queryset(self):
        if self.request.user.role == "STUDENT":
            student_id = StudentProfile.objects.filter(user=self.request.user.id).first()
            return self.queryset.filter(posted_to=student_id.courses)
        if self.request.user.role == "STAFF":
            teacher_id = TeacherProfile.objects.filter(user=self.request.user.id).first()
            return self.queryset.filter(posted_by=teacher_id)
        return super().get_queryset()

class AnnouncementDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AnnouncementListCreateSerializer
    queryset = Announcement.objects.all()

class LessonCreateAPIView(ListCreateAPIView):
    serializer_class = LessonListCreateSerializer
    queryset = Lesson.objects.all()