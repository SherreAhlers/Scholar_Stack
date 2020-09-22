from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('status_create/', views.StatusCreate.as_view(), name='status_create'),
    path('profile/<int:profile_id>/', views.profile_detail, name='profile_detail'),

    path('profile/<int:profile_id>/edit_avatar/', views.edit_avatar, name='edit_avatar'),
    path('profile/<int:profile_id>/create_task/', views.create_task, name='create_task'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # path('accounts/signup/', views.signup, name='signup'),





