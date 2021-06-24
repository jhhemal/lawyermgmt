from django.contrib import admin
from django import forms
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import *

# Register your models here.
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'mobile_no', 'fee', 'exp', 'bio', 'membership_id', 'address', 'image', 'user_type', 'password1', 'password2')}
        ),
    )

UserAdmin.fieldsets += ('User Details', {'fields': ('mobile_no', 'user_type', 'fee', 'exp', 'bio', 'membership_id', 'address', 'image')}),

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Booking)