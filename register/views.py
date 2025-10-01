from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .forms import RegisterForm


def register(request):
    """View to handle user registration (sign-up)."""

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            form.save()  # Saves the new user to the database

            # Get the new user and assign them to the 'LibraryMember' group
            try:
                user = User.objects.get(username=uname)
                # Assumes 'LibraryMember' group has already been created
                lib_group = Group.objects.get(name='LibraryMember')
                user.groups.add(lib_group)
                user.save()
            except Group.DoesNotExist:
                # Handle case where the group isn't created yet
                pass

            # Redirects to the login page after successful registration
            return redirect('login')

            # If the form is invalid, execution will continue to the final render

    else:
        # GET request: Display the empty form
        form = RegisterForm()

    # Renders the registration template using the correct template path
    # 🌟 CHANGE: template name changed from "register/registration.html" to "register/register.html"
    return render(request, "register/register.html", {"form": form})
