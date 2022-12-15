from django.shortcuts import render
from .serializers import (AssignmentDetailSerializer, 
        AssignmentInlineSerializer, AssignmentSerializer, 
        AssignmentWithCourseSerializer)
from .models import Assignment
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from teachers.models import TeacherProfile
from classes.models import Class
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class AssignmentView(ListCreateAPIView):
    queryset = Assignment.objects.all()
    # serializer_class = AssignmentSerializer
    serializer_class = AssignmentWithCourseSerializer
    
    def get_queryset(self):
        teacher_id = TeacherProfile.objects.filter(user=self.request.user.id).first()
        return self.queryset.filter(given_by=teacher_id)

    def perform_create(self, serializer):
        teacher_id = TeacherProfile.objects.filter(user=self.request.user.id).first()
        serializer.save(given_by=teacher_id)

class GetAssignmentsGivenToClassByTeacher(ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        teacher_id = TeacherProfile.objects.filter(user=self.request.user.id).first()
        course = self.request.data.get('course_id')
        get_course = Class.objects.filter(id=course).first()
        if hasattr(get_course, 'id'):
            return self.queryset.filter(given_by=teacher_id, given_to=get_course)
        return Response({'detail':'class not found'}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        teacher_id = TeacherProfile.objects.filter(user=self.request.user.id).first()
        course = self.request.data.get('course_id')
        get_course = Class.objects.filter(id=course).first()
        if hasattr(get_course, 'id'):
            serializer.save(given_by=teacher_id, given_to=get_course)
        return Response({'detail':'class not found'}, status=status.HTTP_404_NOT_FOUND)

class AssignmentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentDetailSerializer

    def get_queryset(self):
        teacher_id = TeacherProfile.objects.filter(user=self.request.user.id).first()
        return self.queryset.filter(given_by=teacher_id)
