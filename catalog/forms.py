# catalog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BookInstance


class LoanBookForm(forms.ModelForm):
    borrower = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        label="Select Borrower"
    )

    class Meta:
        model = BookInstance
        fields = ['borrower']  # ✅ ensure only borrower is exposed


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
