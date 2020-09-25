from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('status_create/', views.ProfileCreationForm.as_view(), name='status_create'),
    path('profile/<int:profile_id>/', views.profile_detail, name='profile_detail'),
    path('profile/<int:profile_id>/edit_avatar/', views.edit_avatar, name='edit_avatar'),
    path('profile/<int:profile_id>/create_task/', views.create_task, name='create_task'),
    path('task_detail/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/update/', views.TaskUpdate.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', views.TaskDelete.as_view(), name='task_delete'),
    path('task_detail/<int:task_id>/create_comment/<int:comment_author_id>', views.create_comment, name='create_comment'),
    path('comment/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment_delete'),
    path('task_doc/<int:task_doc_id>/delete/', views.task_doc_delete, name='task_doc_delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)






