from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

# User Registration Form
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'email', 'username', 'password1', 'password2',
            'full_name', 'phone_number', 'profile_picture', 'role',
        ]

# User Login Form
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'autofocus':True}),
        label="Email"
    )

# User Update Form (Optional)
class UserUpdateForm(forms.ModelForm):
    class Meta: 
        model = CustomUser
        fields = [
            'email', 'username','full_name', 
            'phone_number', 'profile_picture', 'role'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
        }