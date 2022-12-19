from django.shortcuts import render
from .serializers import CourseDetailSerializer, CourseListCreateSerializer
from .models import Course
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# Create your views here.

class CourseView(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListCreateSerializer

class CourseDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer