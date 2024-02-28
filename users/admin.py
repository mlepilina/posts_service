from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'birth_date',)
    list_filter = ('create_date',)
    readonly_fields = ('create_date', 'change_date',)

