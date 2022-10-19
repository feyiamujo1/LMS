from django.shortcuts import render
from .serializers import TeacherCreateSerializer, TeacherDetailSerializer
from .models import Teacher
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
# Create your views here.


class TeacherListCreateView(ListCreateAPIView):
    queryset = Teacher.teachers.all()
    serializer_class = TeacherCreateSerializer

class TeacherDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Teacher.teachers.all()
    serializer_class = TeacherDetailSerializer
