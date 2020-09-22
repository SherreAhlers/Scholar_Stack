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
        # print("status is not empty")
        return True
    else:
        # print("status is empty")
        return False


def home(request):
    if hasattr(request.user, 'profile') and user_has_profile(request, request.user.profile):
    # user_has_profile(request, request.user.profile):
        # print('User is_authenticated and has a profile')
        profile = Profile.objects.get(id=request.user.profile.id)
        # avatar = Profile_Avatar.objects.get(profile_id=request.user.profile.id)
        return redirect('profile_detail', profile_id=profile.id)
    elif request.user.id == None:
        # print('User without profile')
        return redirect('signup')
    else:
        return redirect('status_create')


def about(request):
    return render(request, 'about.html')

def profile_detail(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    return render(request, 'profile_index.html', {'profile': profile})

def edit_avatar(request, profile_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # We need a unic key / but keep the file extention too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case we get an errot
    try:
        s3.upload_fileobj(photo_file, BUCKET, key)
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        # Profile_Avatar.objects.create(url=url, profile_id=profile_id)
        Profile_Avatar.objects.get(profile_id=profile_id).update(url=url)
    except:
        print('An error occured uploading file to S3')
    return redirect('home')


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
