from rest_framework import serializers

from xnote_base.models import Post, Person


class PostSerializer(serializers.ModelSerializer):
    university = serializers.CharField(source='get_university_display')

    class Meta:
        depth = 1
        model = Post
        fields = ('id', 'author', 'title', 'image', 'publish_time', 'context', 'university', 'tags')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('user__formal_name', 'profile_image',)
