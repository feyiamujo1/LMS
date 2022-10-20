from rest_framework import serializers
from .models import Assignment
from django.contrib.auth import get_user_model

User = get_user_model()

class AssignmentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='assignment-detail',
            lookup_field='pk', read_only=True)
    given_to = serializers.StringRelatedField()
    given_by = serializers.StringRelatedField()
            
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

