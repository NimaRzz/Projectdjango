from django import forms
from .models import Post, Comment


class PostUpdateForm(forms.ModelForm):
     class Meta:
         model = Post
         fields = ['title', 'body']

class PostCreateForm(forms.Form):
     title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
     body = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))

class CommentCreateReplayForm(forms.Form):
     body = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))