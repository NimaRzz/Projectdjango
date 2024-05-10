from django.db import models
from accounts.models import User
from ckeditor.fields import RichTextField

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    body = RichTextField()
    slug = models.CharField(max_length=80, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return self.title

    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return f'{self.from_user} liked {self.post.title}'
    
class Comment(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.from_user} - {self.created}'

class CommentReplay(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    replay = models.BooleanField(default=True)
    to_comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='tcomment')
    
    def __str__(self):
        return f'{self.from_user} - {self.created}'

