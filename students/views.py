from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Student
from .serializers import StudentCreateSerializer, StudentDetailSerializer
# Create your views here.

class StudentListCreateView(ListCreateAPIView):
    queryset = Student.students.all()
    serializer_class = StudentCreateSerializer

class StudentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentDetailSerializer