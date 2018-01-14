from django.contrib import admin
from .models import User, Event, Feedback, Comment

class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'email_address', 'level', 'is_superuser', 'is_staff']
    list_filter = ['id', 'level', 'is_superuser', 'is_staff']
    search_fields = ['id', 'nickname', 'email_address']
    filter_horizontal = ['groups', 'user_permissions', 'following_users']

class EventModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']

class FeedbackModelAdmin(admin.ModelAdmin):
    list_display = ['id']

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['id']

admin.site.register(User, UserModelAdmin)
admin.site.register(Event, EventModelAdmin)
admin.site.register(Feedback, FeedbackModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
