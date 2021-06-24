from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

User = get_user_model()

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'address', 'mobile_no', 'image', 'password1', 'password2']

class UpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'address', 'mobile_no', 'image']

class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'

class LawyerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'address', 'category', 'membership_id', 'fee', 'exp', 'bio', 'mobile_no', 'image', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['membership_id'].required = True
        self.fields['category'].required = True

class LawyerUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'address', 'is_active', 'category', 'membership_id', 'fee', 'exp', 'bio', 'mobile_no', 'image']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'service', 'payment_method', 'trxnid', 'amount']

        widgets = {
            'date' : forms.TextInput(attrs={
                'type' : 'date',
            })
        }

class AdminBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

class BookingUpdateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['client', 'lawyer', 'date', 'service', 'payment_method', 'trxnid', 'amount', 'status']

        widgets = {
            'date' : forms.TextInput(attrs={
                'type' : 'date',
            })
        }

class AdminBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']

class ExpertAreaForm(forms.ModelForm):
    class Meta:
        model = ExpertArea
        fields = ['title']