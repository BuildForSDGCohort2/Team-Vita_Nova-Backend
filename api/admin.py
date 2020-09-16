from django.contrib import admin
import api.models as am


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'image')


admin.site.register(am.AppUser, UserAdmin)