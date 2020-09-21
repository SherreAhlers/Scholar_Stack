from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from main_app.forms import ProfileCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def user_has_profile(request, profile):
    print('hitting user.profile', len(profile.status))
    if profile.status:
        print("status is not empty")
        # return True
    else:
        print("status is empty")
        return False

def home(request):
    # print('hitting home', request.user.profile.status)
    if user_has_profile(request, request.user.profile) == True:
        return render(request, 'home.html')
    else:
        return render(request, 'create_status.html')

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