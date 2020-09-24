from django.contrib import admin
import api.models as am


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'image')


class UserReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'users', 'type_of_review', 'comment', 'reviewer', 'rating')

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'user', 'notice_by_users', 'last_interaction')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'user', 'chatroom', 'read_by_users', 'content')

admin.site.register(am.AppUser, UserAdmin)
admin.site.register(am.UserReview, UserReviewAdmin)
admin.site.register(am.ChatRoom, ChatRoomAdmin)
admin.site.register(am.Message, MessageAdmin)
