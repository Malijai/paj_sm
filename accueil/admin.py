from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Projet, Paj
# Register your models here.


class ProjetInline(admin.StackedInline):
    model = Projet
    can_delete = False


class PajsInline(admin.StackedInline):
    model = Paj
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (ProjetInline,PajsInline)
    list_display = ('username', 'email','first_name', 'last_name', 'is_active', 'last_login')
    list_filter = ('is_active',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request,obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

