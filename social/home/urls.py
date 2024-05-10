from django.urls import path
from .views import *

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('post/<int:post_id>/<slug:post_slug>/', PostDetailView.as_view(), name='post_detail'),
    path('delete/<int:post_id>/<slug:post_slug>/', PostDeleteView.as_view(), name='post_delete'),
    path('update/<int:post_id>/<slug:post_slug>/', PostUpdateView.as_view(), name='post_update'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('like/<int:post_id>/', PostLikeView.as_view(), name='post_like'),
    path('unlike/<int:post_id>/', PostUnLikeView.as_view(), name='post_unlike'),
    path('comment/create/<int:post_id>/', CommentCreateView.as_view(), name='comment_add'),
    path('comment/<int:comment_id>/replay/<int:post_id>/', CommentReplayView.as_view(), name='comment_replay'),
] 