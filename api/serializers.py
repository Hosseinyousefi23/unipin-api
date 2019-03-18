from rest_framework import serializers

from api.models import Post, Tag


class PostSerializer(serializers.ModelSerializer):
    university = serializers.CharField(source='get_university_display')

    class Meta:
        depth = 1
        model = Post
        fields = ('id', 'author', 'title', 'image', 'publish_time', 'event_start_time', 'event_end_time', 'event_place',
                  'context', 'university', 'tags', 'event_status',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'description',)
