from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify
from .forms import PostUpdateForm, PostCreateForm, CommentCreateReplayForm
from accounts.models import User
from home.models import Post, Like, Comment, CommentReplay


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts':posts})
    
class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        user = get_object_or_404(User, pk=post.user.id)
        likes = Like.objects.filter(post=post)
        comments = Comment.objects.filter(post=post)
        replay = CommentReplay.objects.filter(post=post)
        like = False
        if Like.objects.filter(from_user=request.user, post=post).exists():
            like = True
            return render(request, 'home/post_detail.html', {'post':post, 'user':user, 'like':like, 'likes':likes, 'comments':comments, 'replay':replay})
        return render(request, 'home/post_detail.html', {'post':post, 'user':user, 'like':like, 'likes':likes, 'comments':comments, 'replay':replay})

class PostDeleteView(LoginRequiredMixin, View):
    
    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        user = get_object_or_404(User, pk=post.user.id)
        if request.user.id != user.id:
            messages.error(request, 'You can\'t delete this post', 'danger')
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id).delete()
        messages.success(request, 'post deleted', 'success')
        return redirect('home:index')

class PostUpdateView(LoginRequiredMixin, View):
    from_class =  PostUpdateForm
    template_name = 'home/post_update.html'
    
    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        user = get_object_or_404(User, pk=post.user.id)
        if request.user.id != user.id:
            messages.error(request, 'You can\'t update this post', 'danger')
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, post_id, post_slug):
        post =  get_object_or_404(Post, pk=post_id)
        form = self.from_class(instance=post)
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, post_id, post_slug):
        post =  get_object_or_404(Post, pk=post_id)
        form = self.from_class(request.POST, instance=post)
        if form.is_valid():
            post.slug = slugify(form.cleaned_data['body'])
            post.save()
            messages.success(request, 'post updated', 'success')
            return redirect('home:post_detail', post.id, post.slug)
        return render(request, self.template_name, {'form':form})

class PostCreateView(LoginRequiredMixin, View):
    from_class =  PostCreateForm
    template_name = 'home/post_create.html'

    def get(self, request):
        form = self.from_class
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.from_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post = Post.objects.create(user=request.user, title=cd['title'], body=cd['body'])
            post.slug = slugify(form.cleaned_data['body'])
            post.save()
            messages.success(request, 'post created', 'success')
            return redirect('home:post_detail', post.id, post.slug)
        return render(request, self.template_name, {'form':form})
        
  
class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
      post = get_object_or_404(Post, pk=post_id)
      like_exists = Like.objects.filter(from_user=request.user, post=post).exists()
      if like_exists:  
         messages.error(request, 'you liked this post', 'danger')
         return redirect('home:post_detail', post.id, post.slug)
      Like.objects.create(post=post, from_user=request.user)
      messages.info(request, 'like', 'info')
      return redirect('home:post_detail', post.id, post.slug)

class PostUnLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
      post = get_object_or_404(Post, pk=post_id)
      like_exists = Like.objects.filter(from_user=request.user, post=post).exists()
      if like_exists:
         get_object_or_404(Like, post=post, from_user=request.user).delete()
         messages.info(request, 'unlike', 'info')
         return redirect('home:post_detail', post.id, post.slug)
      messages.error(request, 'you unliked this post', 'danger')
      return redirect('home:post_detail', post.id, post.slug)

class LikeCountView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        likes = Like.objects.filter(post=post)
        return render(request, 'home/post_detail.html', {'likes':likes})

class CommentCreateView(LoginRequiredMixin, View):
    form_class = CommentCreateReplayForm
    template_name = 'home/comment_add.html'
   
    def get(self, request, post_id):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, post_id):
        form = self.form_class(request.POST)
        post = get_object_or_404(Post, pk=post_id)
        if form.is_valid():
            cd = form.cleaned_data
            comment = Comment.objects.create(body=cd['body'], from_user=request.user, post=post)
            messages.success(request, 'comment created successfully', 'success')
            return redirect('home:post_detail', post.id, post.slug)
        return render(request, self.template_name, {'form':form})

class CommentReplayView(LoginRequiredMixin, View):
    form_class = CommentCreateReplayForm
    template_name = 'home/comment_add.html'

    def get(self, request, comment_id, post_id):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, comment_id, post_id):
        form = self.form_class(request.POST)
        post = get_object_or_404(Post, pk=post_id)
        main_comment = get_object_or_404(Comment, pk=comment_id)
        if form.is_valid():
            cd = form.cleaned_data
            comment = CommentReplay.objects.create(body=cd['body'], from_user=request.user, post=post, replay=True, to_comment=main_comment)
            messages.success(request, 'comment created successfully', 'success')
            return redirect('home:post_detail', post.id, post.slug)
        return render(request, self.template_name, {'form':form})

