from django.shortcuts import render
from .serializers import (AssignmentDetailSerializer, 
        AssignmentInlineSerializer, AssignmentSerializer, 
        AssignmentWithCourseSerializer)
from .models import Assignment
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from teachers.models import TeacherProfile
from students.models import StudentProfile, CourseStudent
from classes.models import Course
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class AssignmentView(ListCreateAPIView):
    queryset = Assignment.objects.all()
    # serializer_class = AssignmentSerializer
    serializer_class = AssignmentWithCourseSerializer
    
    def get_queryset(self):
        if self.request.user.role == "STAFF":
            teacher_id = TeacherProfile.objects.filter(user=self.request.user.id).first()
            return self.queryset.filter(given_by=teacher_id)
        if self.request.user.role == "STUDENT":
            student_id = StudentProfile.objects.filter(user=self.request.user.id).first()
            # course = CourseStudent.objects.filter(student=student_id).all()
            courses = Course.objects.filter(studentship__student=student_id)
            return self.queryset.filter(given_to__in=courses)
        return self.queryset()

    def create(self, request, *args, **kwargs):
        if self.request.user.role == "STAFF":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'detail':'only staff users can give assignments'}, status=status.HTTP_403_FORBIDDEN)

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
        get_course = Course.objects.filter(id=course).first()
        if hasattr(get_course, 'id'):
            return self.queryset.filter(given_by=teacher_id, given_to=get_course)
        return Response({'detail':'course not found'}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        teacher_id = TeacherProfile.objects.filter(user=self.request.user.id).first()
        course = self.request.data.get('course_id')
        get_course = Course.objects.filter(id=course).first()
        if hasattr(get_course, 'id'):
            serializer.save(given_by=teacher_id, given_to=get_course)
        return Response({'detail':'course not found'}, status=status.HTTP_404_NOT_FOUND)

class AssignmentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentDetailSerializer

    def get_queryset(self):
        teacher_id = TeacherProfile.objects.filter(user=self.request.user.id).first()
        return self.queryset.filter(given_by=teacher_id)
