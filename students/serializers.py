from rest_framework import serializers
from django.contrib.auth import get_user_model
from classes.models import Class

from classes.serializers import ClassInlineSerializer
from .models import Student, StudentProfile, ClassStudent
from assignments.models import Assignment
from announcements.models import Announcement

User = get_user_model()

class StudentCreateSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='student-detail', read_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        student = User(**validated_data)
        student.set_password(password)
        student.is_active= True
        student.role = User.Role.STUDENT
        student.save()

        profile = StudentProfile.objects.create(user=student)
        profile.save()
        return student

    class Meta:
        model = Student
        fields = ('id', 'email', 'firstname', 'lastname', 'role', 'url', 'password')


class StudentDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def to_representation(self, instance):
        # print(instance, Class.objects.all().first().students)
        data = super(StudentDetailSerializer, self).to_representation(instance)
        data.update({
            'classes' : ClassInlineSerializer(Class.objects.filter(students__user=instance), many=True, context=self.context).data,
            'assignments': Assignment.objects.filter(given_to__students__user=instance).count(),
            # 'classes' : Class.objects.filter(student__user=instance).count(),
        })

        return data
    
    def update(self, instance, validated_data):
        instance.firstname = validated_data.get('firstname')
        instance.lastname = validated_data.get('lastname')
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance

    class Meta:
        model = Student
        fields = ('email', 'firstname', 'lastname', 'password') 

class ClassStudentCreateSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='studentship-detail', lookup_field='pk', read_only=True)
    student = serializers.StringRelatedField()
    class_name = serializers.StringRelatedField()

    class Meta:
        model = ClassStudent
        fields = ('url', 'student', 'class_name', 'date_added')

