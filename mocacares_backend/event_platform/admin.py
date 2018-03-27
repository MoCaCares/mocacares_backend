from django.contrib import admin
from .models import User, Event, Feedback, Comment, EventType, SystemConfig, Message, UploadedImage, UidVerificationPair
from django.contrib.sessions.models import Session

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']

class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email_address', 'level', 'is_superuser', 'is_staff']
    list_filter = ['level', 'is_superuser', 'is_staff']
    search_fields = ['id', 'username', 'email_address']
    filter_horizontal = ['groups', 'user_permissions', 'following_users']

class EventModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']
    list_filter = ['event_type']
    search_fields = ['id', 'title', 'description']
    filter_horizontal = ['followers', 'participants']

class FeedbackModelAdmin(admin.ModelAdmin):
    list_display = ['id']

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'target_event', 'poster']
    list_filter = ['target_event', 'poster']

class EventTypeModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class SystemConfigModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'is_show_email', 'is_show_events']

class MessageModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'sender', 'receiver', 'content', 'read']
    list_filter = ['sender', 'receiver']

class UploadedImageModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'image_url']

class UidVerificationPairModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'uid', 'verification_code']

admin.site.register(Session, SessionAdmin)

admin.site.register(User, UserModelAdmin)
admin.site.register(Event, EventModelAdmin)
admin.site.register(Feedback, FeedbackModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
admin.site.register(EventType, EventTypeModelAdmin)
admin.site.register(SystemConfig, SystemConfigModelAdmin)
admin.site.register(Message, MessageModelAdmin)
admin.site.register(UploadedImage, UploadedImageModelAdmin)
admin.site.register(UidVerificationPair, UidVerificationPairModelAdmin)








