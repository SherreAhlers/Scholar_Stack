import uuid
import boto3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from main_app.forms import ProfileCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import User, Profile, Profile_Avatar, Task, Comment, Task_Doc
from .forms import TaskForm, ProfileCreationForm, CommentForm, Task_DocForm

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'scholarstack'
# Create your views here.


def user_has_profile(request, profile):
    if profile.status:
        return True
    else:
        return False


def home(request):
    if request.user.id and not hasattr(request.user, 'profile'):
        return redirect('status_create')
    else:
        return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def add_task_photo(request, task_id):
    task_doc = request.FILES.get('task_doc', None)
    if task_doc:
        s3 = boto3.client('s3')
        # We need a unic key / but keep the file extention too
        key = uuid.uuid4().hex[:6] + task_doc.name[task_doc.name.rfind('.'):]
        # just in case we get an errot
    try:
        s3.upload_fileobj(task_doc, BUCKET, key)
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        Task_Doc.objects.create(url=url, task_id=task_id)
    except:
        print('An error occured uploading file to S3')
    else:
        pass

def task_doc_delete(request, task_doc_id):
    task_doc = Task_Doc.objects.get(id=task_doc_id)
    task_id = task_doc.task.id
    task_doc.delete()
    return redirect('task_detail', task_id=task_id)


def profile_detail(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    task_form = TaskForm()
    task_doc_form = Task_DocForm()
    student_tasks = Task.objects.filter(author=profile_id).order_by('-date_created')
    tutor_tasks = Task.objects.all().order_by('-date_created')
    return render(request, 'profile_index.html', {'profile': profile, 'task_form': task_form, 'task_doc_form': task_doc_form, 'student_tasks': student_tasks, 'tutor_tasks': tutor_tasks})


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
        new_task.author_id = profile_id
        new_task.save()
    task = Task.objects.latest('date_created')
    add_task_photo(request, task.id)
    return redirect('profile_detail', profile_id=profile_id)


def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    task_docs = Task_Doc.objects.filter(task_id=task_id)
    comments = Comment.objects.filter(
        task_id=task_id).order_by('-date_created')
    comment_form = CommentForm()
    return render(request, 'task_detail.html', {'task': task, 'task_docs': task_docs, 'comments': comments, 'comment_form': comment_form})
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'level', 'field', 'body']
    def get_success_url(self):
        task = self.get_object()
        return reverse('task_detail', kwargs={'task_id': task.id})

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    def get_success_url(self):
        task = self.get_object()
        return reverse('profile_detail', kwargs={'profile_id': task.author.id})

def create_comment(request, task_id, comment_author_id):
    task = Task.objects.get(id=task_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.author_id = comment_author_id
        new_comment.task_id = task_id
        new_comment.save()
    return redirect('task_detail', task_id=task_id)

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['body']
    def get_success_url(self):
        comment = self.get_object()
        return reverse('task_detail', kwargs={'task_id': comment.task.id})

class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    def get_success_url(self):
        comment = self.get_object()
        return reverse('task_detail', kwargs={'task_id': comment.task.id})


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

class ProfileCreationForm(CreateView):
    model = Profile
    fields = ['status']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
