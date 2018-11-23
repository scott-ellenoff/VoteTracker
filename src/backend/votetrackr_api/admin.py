from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Bill, Legislator, Vote, User

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('district',)}),
    )
    model = User
    list_display = ['email', 'username', 'UID', 'district',]

# Register your models here.
admin.site.register(Bill)
admin.site.register(Legislator)
admin.site.register(Vote)
admin.site.register(User, CustomUserAdmin)