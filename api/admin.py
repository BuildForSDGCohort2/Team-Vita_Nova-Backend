from django.contrib import admin
import api.models as am


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'image')


class UserReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'user', 'type_of_review', 'comment', 'reviewer', 'rating')

class ChatRoomAdmin(admin.ModelAdmin):
    pass

admin.site.register(am.AppUser, UserAdmin)
admin.site.register(am.UserReview, UserReviewAdmin)
admin.site.register(am.ChatRoom, ChatRoomAdmin)
