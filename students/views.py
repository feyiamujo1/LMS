from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import ClassStudent, Student
from .serializers import ClassStudentCreateSerializer, StudentCreateSerializer, StudentDetailSerializer
# Create your views here.

class StudentListCreateView(ListCreateAPIView):
    queryset = Student.students.all()
    serializer_class = StudentCreateSerializer

class StudentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentDetailSerializer

class ClassStudentCreateListView(ListCreateAPIView):
    queryset = ClassStudent.objects.all()
    serializer_class = ClassStudentCreateSerializer

class ClassStudentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ClassStudent.objects.all()
    serializer_class = ClassStudentCreateSerializer

