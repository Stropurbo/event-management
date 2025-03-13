from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class CustomRegisterForm(forms.ModelForm): # it is field error
    password = forms.CharField()
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

        help_texts = {
            'username' : None
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError("Password Length atleast 8")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password atleast One Uppercase")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Password atlease one lowercase")
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("Password include one Number")
        if not re.search(r'[@$%^&*+#]', password):
            raise forms.ValidationError("Password must be atleast one special character")

        return password

    def clean(self):
        cleaned_data = super().clean()    

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error("email", "This email already registerd")
            raise forms.ValidationError("E-mail Already in use")
        
        if password != confirm_password:
            self.add_error('password', 'Password do not match')
            raise forms.ValidationError("Password do not match")
        
        return cleaned_data
    
    def save(self, commit =True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password']) 
        if commit:
            user.save()
        return user