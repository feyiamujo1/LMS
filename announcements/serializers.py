from rest_framework import serializers
from .models import Announcement


class AnnouncementListCreateSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='announcement-detail', read_only=True)
    posted_to = serializers.StringRelatedField()
    posted_by = serializers.StringRelatedField()
    class Meta:
        model = Announcement
        fields = ('url','title','posted_by', 'posted_to', 'body', 'attachment', 'date')

class AnnouncementInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='announcement-detail', read_only=True)
    title = serializers.CharField(read_only=True)
    posted_by = serializers.StringRelatedField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
