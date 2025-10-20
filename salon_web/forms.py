from django import forms
from .models import Customer

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone', 'address', 'referral_code']  # Add any other fields you want the user to be able to edit

    # Optional: You can add custom validation or widget styling if needed
