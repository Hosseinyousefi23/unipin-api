from django.contrib import admin

from api.models import Tag, Post


admin.site.register(Tag)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('id', 'title', 'image',)
