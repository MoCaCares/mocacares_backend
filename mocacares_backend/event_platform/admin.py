from django.contrib import admin
from .models import User, Event, Feedback, Comment, EventType, SystemConfig, Message, UploadedImage, TokenVerificationPair
from django.contrib.sessions.models import Session

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']

class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email_address', 'level', 'is_superuser', 'is_staff']
    list_filter = ['id', 'level', 'is_superuser', 'is_staff']
    search_fields = ['id', 'username', 'email_address']
    filter_horizontal = ['groups', 'user_permissions', 'following_users']

class EventModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']

class FeedbackModelAdmin(admin.ModelAdmin):
    list_display = ['id']

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['id']

class EventTypeModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class SystemConfigModelAdmin(admin.ModelAdmin):
    pass

class MessageModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'sender', 'receiver', 'content', 'read']

class UploadedImageModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'image_url']

class TokenVerificationPairModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'token', 'verification_code']

admin.site.register(Session, SessionAdmin)

admin.site.register(User, UserModelAdmin)
admin.site.register(Event, EventModelAdmin)
admin.site.register(Feedback, FeedbackModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
admin.site.register(EventType, EventTypeModelAdmin)
admin.site.register(SystemConfig, SystemConfigModelAdmin)
admin.site.register(Message, MessageModelAdmin)
admin.site.register(UploadedImage, UploadedImageModelAdmin)
admin.site.register(TokenVerificationPair, TokenVerificationPairModelAdmin)








