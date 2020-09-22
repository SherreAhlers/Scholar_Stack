import uuid
import boto3
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from main_app.forms import ProfileCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Profile

S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'
BUCKET = 'scholarstack'
# Create your views here.


def user_has_profile(request, profile):
    # print('hitting user.profile', len(profile.status))
    if profile.status:
        print("status is not empty")
        return True
    else:
        print("status is empty")
        return False


def home(request):
    if hasattr(request.user, 'profile') and user_has_profile(request, request.user.profile):
    # user_has_profile(request, request.user.profile):
        print('User is_authenticated and has a profile')
        return render(request, 'profile_index.html')
    elif request.user.id == None:
        print('User without profile')
        return redirect('signup')
    else:
        return redirect('status_create')


def about(request):
    return render(request, 'about.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


class StatusCreate(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['status']
