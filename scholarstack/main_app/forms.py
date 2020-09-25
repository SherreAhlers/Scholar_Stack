from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.core.files.images import get_image_dimensions
from .models import Profile, Task, Comment, Task_Doc


class ProfileCreationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['status']


class ProfileChangeForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = ['status']


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'field', 'level', 'body']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class Task_DocForm(ModelForm):
    class Meta:
        model = Task_Doc
        fields = ['url']
