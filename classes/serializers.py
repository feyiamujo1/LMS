from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from students.models import Student, StudentProfile, ClassStudent
from .models import Class
from teachers.models import Teacher

# factory = APIRequestFactory()
# request = factory.get('/')

class TeacherInlineSerializer(serializers.Serializer):
    # url = serializers.HyperlinkedIdentityField(view_name='teacher-detail', lookup_field='pk', read_only=True)
    email = serializers.EmailField(read_only=True)
    firstname = serializers.CharField(read_only=True)
    lastname = serializers.CharField(read_only=True)

class StudentshipDetailViewSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='studentship-detail', lookup_field='pk', read_only=True)

    class Meta:
        model = ClassStudent
        fields = ('url',)

class StudentInlineSerializer(serializers.Serializer):
    firstname = serializers.CharField(read_only=True)
    lastname = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    def to_representation(self, instance):
        data = super(StudentInlineSerializer, self).to_representation(instance)
        student = StudentProfile.objects.filter(user=instance).first()
        data.update({
            'picture': student.picture or None,
            'id' : student.student_id or None,
        })

        return data

class ClassSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='class-detail', lookup_field='pk', read_only=True)
    created_by = serializers.StringRelatedField()

    def to_representation(self, instance):
        data = super(ClassSerializer, self).to_representation(instance)
        data.update({
            'teachers': TeacherInlineSerializer(Teacher.objects.filter(teacherprofile__adminship__class_name=instance), many=True).data,
            'students': StudentInlineSerializer(Student.objects.filter(studentprofile__classes__id=instance.id), many=True).data,
        })

        return data
    class Meta:
        model = Class
        fields = ('url','id', 'name', 'session', 'created_by')

class ClassInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='class-detail', lookup_field='pk', read_only=True)
    name = serializers.CharField(read_only=True)
    session = serializers.CharField(read_only=True)