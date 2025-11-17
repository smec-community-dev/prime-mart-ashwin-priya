from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


class SellerUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'seller'  
        if commit:
            user.save()
        return user


# 2️⃣ Form for Seller Profile
class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['name', 'address'] 
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Shop Name'}),
            'address': forms.Textarea(attrs={'placeholder': 'Shop Address'}),
        }

class SellerLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"})
    )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Product Name', 'class': 'w-full px-4 py-2 border rounded-lg'}),
            'description': forms.Textarea(attrs={'placeholder': 'Product Description', 'class': 'w-full px-4 py-2 border rounded-lg', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'stock': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image_file']
        widgets = {
            'image_file': forms.ClearableFileInput(),  
        }
