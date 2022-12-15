from rest_framework import serializers
from .models import Assignment
from django.contrib.auth import get_user_model

User = get_user_model()

class AssignmentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='assignment-detail',
            lookup_field='pk', read_only=True)
    # given_to = serializers.StringRelatedField()
    # given_by = serializers.StringRelatedField()
            
    class Meta:
        model = Assignment
        fields = ('url', 'given_by', 'title', 'body', 'attachment', 
        'given_to', 'given_on', 'deadline')

class AssignmentDetailSerializer(serializers.ModelSerializer):
    given_by = serializers.StringRelatedField()
    given_to = serializers.StringRelatedField()

    class Meta:
        model = Assignment
        fields = ('given_by', 'title', 'body', 'attachment', 
        'given_to', 'given_on', 'deadline')


class AssignmentInlineSerializer(serializers.Serializer):
    given_by = serializers.StringRelatedField(read_only=True)
    title = serializers.CharField(read_only=True)
    deadline = serializers.DateTimeField(read_only=True)

class UserProfileField(serializers.RelatedField):
    def to_representation(self, value):
        return {'id':value.pk, 'user name': f"{value.user.firstname} {value.user.lastname}"}

class ClassField(serializers.RelatedField):
    def to_representation(self, value):
        return {'id': value.pk, 'class name': value.name}

class AssignmentWithCourseSerializer(serializers.ModelSerializer):
    teacher = UserProfileField(read_only=True, source='given_by')
    course = ClassField(read_only=True, source='given_to')
    class Meta:
        model = Assignment
        fields = ('given_by', 'title', 'body', 'attachment', 
            'given_to', 'given_on', 'deadline', 'course', 'teacher')
