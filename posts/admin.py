from django.contrib import admin
from django.utils.safestring import mark_safe

from posts.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'create_date', 'get_image',)
    list_filter = ('create_date',)
    readonly_fields = ('create_date', 'change_date', 'get_image',)

    def get_image(self, obj):
        url = obj.image and obj.image.url
        return mark_safe(f'<a target="_blank" href="{url}"><img src={url} width="70" height="60"</a>')

    get_image.short_description = 'Изображение'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text',)

