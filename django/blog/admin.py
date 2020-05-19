from django.contrib import admin
from . import models
from django.utils.html import mark_safe
from django_summernote.admin import SummernoteModelAdmin

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'category', 'title', 'likes', 'dislikes', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'category')
    list_display_links = ('title',)
    list_per_page = 10
    # summernote_fields = ('content',)
    # search_fields = ('title', 'content')
    date_hierarchy = 'publish'
    ordering = ('status', '-publish')

    def image_tag(self, obj):
        try:
            return mark_safe(f'<img src="{obj.image.url}" width="80" height="60"/>')
        except Exception as err:
            print(err.__class__)
            pass

    image_tag.short_description = 'Фото'



admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.IpUser)

