from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserLoginForm, UserRegisterForm, UserDeleteAccountForm, VerifyUserRegisterForm, UserPasswordChangeForm, VerifyUserPasswordChangeForm, UserPasswordChangeCompleteForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from .models import OtpCode

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/user_login.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
          cd = form.cleaned_data
          user=authenticate(request, username=cd['phone'], password=cd['password'])
          if user is not None:
              login(request, user)
              messages.success(request, 'You are logined successfully', 'success')
              if request.GET.get('next') is not None:
                  return redirect(request.GET.get('next'))
              return redirect('home:index')
          messages.error(request, 'username or password is wrong', 'danger')
        return render(request, self.template_name, {'form':form})
        


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/user_register.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
          cd = form.cleaned_data
          code = random.randint(1000, 9999)
          OtpCode.objects.create(code=code, phone=cd['phone'])
          request.session['verify_user_register'] = {
              'phone':cd['phone'],
              'email':cd['email'],
              'fullname':cd['fullname'],
              'password':cd['password1'],
              'code':code
          }
          messages.success(request, f"we have sent code to {cd['phone']}", 'success')
          messages.info(request, "سایت به سرویس ارسال پیامک وصل نیست تویه منویه ادمینی تویه او تی پی کدز کد رو وردارین  ", 'info')
          return redirect('accounts:verify_user_register')
        return render(request, self.template_name, {'form':form})
      

class VerifyUserRegisterView(View):
    form_class = VerifyUserRegisterForm
    template_name = 'accounts/verify_user_register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
      form = self.form_class
      return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():  
          session = request.session['verify_user_register']
          cd = form.cleaned_data
          if cd['otp_code'] == session['code']:
           get_object_or_404(OtpCode, phone=session['phone'], code=session['code']).delete()
           user = User.objects.create(phone=session['phone'], email=session['email'], fullname=session['fullname'])
           user.set_password(session['password'])
           user.save()
           messages.success(request, 'You are registred successfully', 'success')
           return redirect('accounts:user_login')
          messages.error(request, 'code is wrong', 'danger')
        return render(request, self.template_name, {'form':form})  
        

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you are logged out successfully', 'success')
        return redirect('accounts:user_login')


class UserDeleteAccountView(LoginRequiredMixin, View):
    form_class = UserDeleteAccountForm
    template_name = 'accounts/user_delete.html'

    def get(self, request, user_id):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, user_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['phone'], password=cd['password'])
            if user is not None:
                if user.id == request.user.id:
                 user.delete()
                 messages.success(request, 'your account deleted successfully', 'success')
                 return redirect('accounts:user_login')
                messages.error(request, 'username or password is wrong', 'danger')
        return render(request, self.template_name, {'form':form})
                
class UserPasswordChangeView(View):
    form_class = UserPasswordChangeForm
    template_name = 'accounts/user_password_change.html'


    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.filter(phone=cd['phone']).exists()
            if user is not None:
                code = random.randint(1000, 9999)
                OtpCode.objects.create(phone=cd['phone'], code=code)
                request.session['password_change'] = {
                    'phone':cd['phone'],
                    'code':code,
                }
                messages.success(request, f'we have sent code to {cd['phone']}', 'success')
                messages.info(request, "سایت به سرویس ارسال پیامک وصل نیست تویه منویه ادمینی تویه او تی پی کدز کد رو وردارین  ", 'info')
                return redirect('accounts:password_change_verify')
        return render(request, self.template_name, {'form':form})
    

class VerifyUserPasswordChangeView(View):
    form_class = VerifyUserPasswordChangeForm
    template_name = 'accounts/verify_user_password_change.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            session = request.session['password_change']
            if session['code'] == cd['otp_code']:
             get_object_or_404(OtpCode, phone=session['phone'], code=session['code']).delete()
             messages.success(request, 'code is True', 'success')
             return redirect('accounts:password_change_complete')
            messages.error(request, 'code is wrong', 'danger')
            return render(request, self.template_name, {'form':form})
        return render(request, self.template_name, {'form':form})

class UserPasswordChangeCompleteView(View):
    form_class = UserPasswordChangeCompleteForm
    template_name = 'accounts/user_password_change_complete.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone = request.session['password_change']['phone']
            user = get_object_or_404(User, phone=phone)
            user.set_password(cd['password1'])
            user.save()
            messages.success(request, 'your password changed successfully', 'success')
            return redirect('accounts:user_login')
        return render(request, self.template_name, {'form':form})