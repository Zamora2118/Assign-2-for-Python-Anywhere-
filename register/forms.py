from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegisterForm(UserCreationForm):
    # This class inherits all fields (username, password, password confirmation)
    # from UserCreationForm. We can add custom fields if necessary, but
    # for a basic assignment, this is usually enough.

    # You can add a placeholder to make the form look better
    # email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    class Meta(UserCreationForm.Meta):
        # We explicitly tell the form to use the fields from the UserCreationForm
        # but we can optionally add 'email' here if we wanted to collect it
        fields = UserCreationForm.Meta.fields