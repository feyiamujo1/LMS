from django.shortcuts import render
from .serializers import TeacherCreateSerializer
from .models import Teacher
from rest_framework.generics import ListCreateAPIView
# Create your views here.


class TeacherCreateView(ListCreateAPIView):
    queryset = Teacher.teachers.all()
    serializer_class = TeacherCreateSerializer