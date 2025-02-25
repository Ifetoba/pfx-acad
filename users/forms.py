from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

# User Registration Form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    full_name = forms.CharField(max_length=255)

    class Meta:
        model = CustomUser
        fields = [
            'full_name', 'username', 'email',
            'phone_number','password1', 'password2',
        ]

# User Login Form
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'autofocus':True,
            'class': 'form-md-control',
            'placeholder': 'Enter your email'}),
        label="Email"
    )
    # password = forms.CharField(
    #     widget=forms.PasswordInput(attrs={
    #       'autofocus':True,
    #         'class': 'form-md-control',
    #         'placeholder': 'Enter your password'  
    #     }))

# User Update Form (Optional)
class UserUpdateForm(forms.ModelForm):
    class Meta: 
        model = CustomUser
        fields = [
            'email', 'username','full_name', 
            'phone_number', 'role'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
        }