from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Transaction


@admin.register(get_user_model())
class UserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('wallet', 'balance')
    fieldsets = UserAdmin.fieldsets + (('Доп. поля', {'fields': ('wallet', 'balance')}),)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
