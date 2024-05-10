from django.urls import path
from .views import *

app_name = 'profiles'

urlpatterns = [
    path('profile/<int:user_id>/', ProfileView.as_view(), name='user_profile'),
    path('unfollow/<int:user_id>/', UnFollowView.as_view(), name='user_unfollow'),
    path('follow/<int:user_id>/', FollowView.as_view(), name='user_follow'),
    path('followers/<int:user_id>/', FollowersView.as_view(), name='user_followers'),
    path('followings/<int:user_id>/', FollowingsView.as_view(), name='user_followings'),
] 