from rest_framework import serializers

from xnote_base.models import Post, Person


class PostSerializer(serializers.ModelSerializer):
    university = serializers.CharField(source='get_university_display')

    # event_status = serializers.SerializerMethodField('get_status')

    class Meta:
        depth = 1
        model = Post
        fields = ('id', 'author', 'title', 'image', 'publish_time', 'event_start_time', 'event_end_time', 'event_place',
                  'is_expired', 'context', 'university', 'tags', 'event_status')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('formal_name', 'profile_image', 'url_name',)
