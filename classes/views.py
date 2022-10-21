from django.shortcuts import render
from .serializers import ClassDetailSerializer, ClassListCreateSerializer
from .models import Class
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# Create your views here.

class ClassView(ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassListCreateSerializer

class ClassDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassDetailSerializer