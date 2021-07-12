from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from.models import Profile
from django.forms import fields
from . models import Post

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','bio']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
    # image = forms.ImageField()
    # image_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Image Name"}))
    # image_caption = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control","placeholder": "Image Caption"}))

class CommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control","placeholder": "Leave a comment!"}))
