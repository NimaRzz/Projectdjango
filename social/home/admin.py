from django.contrib import admin
from .models import Post, Like, Comment, CommentReplay

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
   
class CommentReplayInline(admin.StackedInline):
    model = CommentReplay
    extra = 0

class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created', 'updated']
    prepopulated_fields = {'slug':['body']}
    raw_id_fields = ['user']
    search_fields = ['title']

    inlines = [
        CommentInline,
        CommentReplayInline
    ]
    
class LikeAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'post']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_user', 'post', 'created']
   
class CommentReplayAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_user', 'post', 'created', 'replay']

admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentReplay, CommentReplayAdmin)