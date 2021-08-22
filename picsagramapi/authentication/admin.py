from django.contrib import admin
from .models import User
from rest_framework_simplejwt.token_blacklist import models
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email']
class NewOutstandingTokenAdmin(OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(models.OutstandingToken)
admin.site.register(models.OutstandingToken, NewOutstandingTokenAdmin)
admin.site.register(User,UserAdmin)
