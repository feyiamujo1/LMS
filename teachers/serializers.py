from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Teacher, TeacherProfile
from classes.models import Class
from assignments.models import Assignment
from announcements.models import Announcement

User=get_user_model()

class TeacherCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        teacher = Teacher.objects.create_user(email=email, password=password)
        teacher.is_active = True
        teacher.role = User.Role.STAFF
        teacher.save()

        profile = TeacherProfile.objects.create(user=teacher)
        profile.save()
        return teacher

    class Meta:
        model = Teacher
        fields = ('email','firstname','lastname','role','password')

class TeacherDetailSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super(TeacherDetailSerializer, self).to_representation(instance)
        data.update({
            'classes': Class.objects.filter(teachers__user=instance),
            'assignments_given': Assignment.objects.filter(given_by__user=instance),
            'announcements': Announcement.objects.filter(posted_by__user=instance)
        })

        return data
    class Meta:
        model = Teacher
        fields = ('email','firstname','lastname','role')