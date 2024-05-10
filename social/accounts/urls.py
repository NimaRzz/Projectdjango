from django.urls import path
from .views import UserRegisterView, VerifyUserRegisterView, UserLoginView, UserLogoutView, UserDeleteAccountView, UserPasswordChangeView, VerifyUserPasswordChangeView, UserPasswordChangeCompleteView

app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('verify_register/', VerifyUserRegisterView.as_view(), name='verify_user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('user/delete/<int:user_id>', UserDeleteAccountView.as_view(), name='user_delete'),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('verify_password_change/', VerifyUserPasswordChangeView.as_view(), name='password_change_verify'),
    path('password_change_complete/', UserPasswordChangeCompleteView.as_view(), name='password_change_complete'),
] 