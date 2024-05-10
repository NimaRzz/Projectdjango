from typing import Any
from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreateForm(forms.ModelForm):
    
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'password'}))
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'confirm password'}))
    
    class Meta:
        model = User
        fields = ['phone', 'email', 'fullname', 'last_login']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('passwords not equal')
        return password1
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="you can change password this <a href=\'../password/\'>form</a>")

    class Meta:
        model = User
        fields = ['phone', 'email', 'fullname', 'password', 'last_login', 'is_admin', 'is_active']


class UserLoginForm(forms.Form):
    phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'phone'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'password'}))


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'password'}))
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'confirm password'}))

    
    class Meta:
        model = User
        fields = ['phone', 'email', 'fullname']

        widgets = { 
            'phone' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'phone'}),
            'email' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'email'}),
            'fullname' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'fullname'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('passwords not equal')
        return password1
    
    def save(self, commit=True):
         user = super().save(commit=False)
         user.set_password(self.cleaned_data['password1'])
         if commit:
          user.save()
         return user
    
    def clean_phone(self):
        cd = self.cleaned_data
        user = User.objects.filter(phone=cd['phone']).exists()
        if user:
            raise ValidationError('this phone already exists')
        return cd['phone']
    
    def clean_email(self):
        cd = self.cleaned_data
        user = User.objects.filter(email=cd['email']).exists()
        if user:
            raise ValidationError('this email already exists')
        return cd['email']





class VerifyUserRegisterForm(forms.Form):
    otp_code = forms.IntegerField(label='code' ,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'code'}))


class UserDeleteAccountForm(forms.Form):
    phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'phone'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'password'}))

class UserPasswordChangeForm(forms.Form):
    phone = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'phone'}))


class VerifyUserPasswordChangeForm(forms.Form):
     otp_code = forms.IntegerField(label='code' ,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'code'}))

class UserPasswordChangeCompleteForm(forms.Form):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'password'}))
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'confirm password'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password2 != password1:
            raise ValidationError('passwrods not equal')
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user