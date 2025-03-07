from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, UserProfile

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
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
          'autofocus':True,
            'class': 'form-md-control',
            'placeholder': 'Enter your password'  
        }))

# User Update Form (Optional)
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["full_name", "email"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class":"form-control"}),
            "email": forms.EmailInput(attrs={"class":"form-control"})
        }


class UserProfileForm(forms.ModelForm):
    class Meta: 
        model = UserProfile
        fields = ["first_name", "last_name", "bio", "profile_picture"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class":"form-control"}),
            "last_name": forms.TextInput(attrs={"class":"form-control"}),
            "bio": forms.Textarea(attrs={"class":"form-control"}),
            "profile_picture": forms.FileInput(attrs={"class":"form-control"}),
        }