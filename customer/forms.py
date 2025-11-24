from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Customer

User = get_user_model()


# ------------------------------
# User Registration Form
# ------------------------------
class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User   # FIXED: Signup should create a USER
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'   # custom field in your User model
        if commit:
            user.save()
        return user


# ------------------------------
# Customer Profile Form
# ------------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone', 'address']

class CustomerLoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"placeholder": "Enter username"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"})
    )
