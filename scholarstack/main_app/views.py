import uuid
import boto3
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from main_app.forms import ProfileCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import User, Profile, Profile_Avatar, Task, Comment
from .forms import TaskForm, ProfileCreationForm, CommentForm

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
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
    if request.user.id and not hasattr(request.user, 'profile'):
        return redirect('status_create')
    else:
        return render(request, 'home.html')

# def home(request):
#     if hasattr(request.user, 'profile') and user_has_profile(request, request.user.profile):
#     # user_has_profile(request, request.user.profile):
#         # print('User is_authenticated and has a profile')
#         profile = Profile.objects.get(id=request.user.profile.id)
#         # avatar = Profile_Avatar.objects.get(profile_id=request.user.profile.id)
#         return redirect('profile_detail', profile_id=profile.id)
#     elif request.user.id == None:
#         # print('User without profile')
#         return redirect('login')
#     else:
#         # profile = Profile.objects.get(id=request.user.profile.id)
#         return redirect('status_create')


def about(request):
    return render(request, 'about.html')


def profile_detail(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    task_form = TaskForm()
    tasks = Task.objects.filter(author=profile_id).order_by('-date_created')
    return render(request, 'profile_index.html', {'profile': profile, 'task_form': task_form, 'tasks': tasks})


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
        avatar, created = Profile_Avatar.objects.get_or_create(profile_id=profile_id, defaults={'url': 'https://i.imgur.com/qx38J6i.png'})
        if created:
            return redirect('profile_detail', profile_id=profile_id)
        else:
            avatar.url = url
            avatar.save()
    except:
        print('An error occured uploading file to S3')
    return redirect('profile_detail', profile_id=profile_id)


def create_task(request, profile_id):
    form = TaskForm(request.POST)
    if form.is_valid():
        new_task = form.save(commit=False)
        # new_task.author = profile_id
        new_task.author_id = profile_id
        new_task.save()
    return redirect('profile_detail', profile_id=profile_id)


def task_detail(request, task_id, task_author_id):
    # task = Task.objects.get(id=task_id)
    task = Task.objects.get(id=task_id)
    comments = Comment.objects.filter(
        task_id=task_id).order_by('-date_created')
    comment_form = CommentForm()
    return render(request, 'task_detail.html', {'task': task, 'comments': comments, 'comment_form': comment_form})


def create_comment(request, task_id, comment_author_id):
    author = User.objects.get(id=comment_author_id)
    task = Task.objects.get(id=task_id)
    # task = Task.objects.get(task_id=task_id)
    task_author_id = task.author_id
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.author_id = comment_author_id
        new_comment.task_id = task_id
        new_comment.save()
    return redirect('task_detail', task_id=task_id, task_author_id=task_author_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('status_create')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
# def status_create(request, profile_id):
#     form = ProfileCreationForm(request.POST)
#     if form.is_valid():
#         new_profile_status = form.save(commit=False)
#         new_profile_status.profile_id = profile_id
#         new_profile_status.save()
#     return redirect('profile_detail', profile_id=profile_id)


class ProfileCreationForm(CreateView):
    model = Profile
    fields = ['status']

    def form_valid(self, form):
        # print(self.request.user.id, '<- this is self.request.user.id')
        form.instance.user = self.request.user
        return super().form_valid(form)
