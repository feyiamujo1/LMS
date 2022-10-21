from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from announcements.models import Announcement

from announcements.serializers import AnnouncementListCreateSerializer
# Create your views here.

class AnnouncementListCreateView(ListCreateAPIView):
    serializer_class = AnnouncementListCreateSerializer
    queryset = Announcement.objects.all()

class AnnouncementDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AnnouncementListCreateSerializer
    queryset = Announcement.objects.all()