from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Relation
from django.contrib import messages
from home.models import Post

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        posts = Post.objects.filter(user=user)
        followers = Relation.objects.filter(to_user=user)
        followings = Relation.objects.filter(from_user=user)
        relation_exists = Relation.objects.filter(from_user=request.user, to_user=user).exists()
        if relation_exists:
            relation = get_object_or_404(Relation, from_user=request.user, to_user=user)
            relation.relation = True
            return render(request, 'profiles/profile.html', {'user':user, 'relation':relation, 'posts':posts, 'followers':followers, 'followings':followings})
        relation = False
        return render(request, 'profiles/profile.html', {'user':user, 'relation':relation, 'posts':posts, 'followers':followers, 'followings':followings})
    
class UnFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
       user = get_object_or_404(User, pk=user_id)
       relation = Relation.objects.filter(from_user=request.user, to_user=user).exists()
       if relation:
           get_object_or_404(Relation, from_user=request.user, to_user=user).delete()
           messages.info(request, 'unfollow', 'info')
           return redirect('profiles:user_profile', user_id)
       messages.error(request, 'you not followed this user', 'danger')
       return redirect('profiles:user_profile', user_id)

class FollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
       user = get_object_or_404(User, pk=user_id)
       relation = Relation.objects.filter(from_user=request.user, to_user=user).exists()
       if relation: 
           messages.error(request, 'you followed this user', 'danger')
           return redirect('profiles:user_profile', user_id)
       Relation.objects.create(from_user=request.user, to_user=user, relation=True)
       messages.info(request, 'follow', 'info')
       return redirect('profiles:user_profile', user_id)

class FollowersView(LoginRequiredMixin, View):
    def get(self, request, user_id):
       user = get_object_or_404(User, pk=user_id)
       followers = Relation.objects.filter(to_user=user)
       if followers.exists():
           followers = Relation.objects.filter(to_user=user)
           return render(request, 'profiles/followers.html', {'followers':followers})
       return render(request, 'profiles/followers.html', {'followers':followers})

class FollowingsView(LoginRequiredMixin, View):
    def get(self, request, user_id):
       user = get_object_or_404(User, pk=user_id)
       followings = Relation.objects.filter(from_user=user)
       if followings.exists():
           followings = Relation.objects.filter(from_user=user)
           return render(request, 'profiles/followings.html', {'followings':followings})
       return render(request, 'profiles/followings.html', {'followings':followings})
