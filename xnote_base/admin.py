from django.contrib import admin

from xnote_base.models import Person, Tag, Post

admin.site.register(Person)
admin.site.register(Tag)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('id', 'title', 'image',)
