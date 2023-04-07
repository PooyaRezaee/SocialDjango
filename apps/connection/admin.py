from django.contrib import admin
from .models import Follow

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('following','follower','in_request')
    list_filter = ('in_request',)