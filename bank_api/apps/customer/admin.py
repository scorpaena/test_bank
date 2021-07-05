from django.contrib import admin
from django.contrib.auth.models import User


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_staff', 'is_active')
    list_filter = ('username', 'is_staff', 'is_active')
    search_fields = ('username',)

admin.site.unregister(User)
admin.site.register(User, CustomerAdmin)
