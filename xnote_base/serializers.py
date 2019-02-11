from rest_framework.serializers import ModelSerializer

from xnote_base.models import Post, Person


class PostSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = Post
        fields = ('id', 'author', 'title', 'image', 'context', 'tags',)


class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = ('user__formal_name', 'profile_image',)
