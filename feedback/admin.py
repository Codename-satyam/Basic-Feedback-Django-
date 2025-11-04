from django.contrib import admin
from .models import Region, MediaOutlet, Story, Feedback

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(MediaOutlet)
class MediaOutletAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'website')
    list_filter = ('region',)
    search_fields = ('name',)

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'outlet', 'published_date')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'excerpt')
    list_filter = ('outlet',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('story', 'user', 'region', 'average_score', 'created_at')
    list_filter = ('region', 'anonymous')
    search_fields = ('comment',)