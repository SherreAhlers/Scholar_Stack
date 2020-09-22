from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('status_create/', views.StatusCreate.as_view(), name='status_create'),

    # path('accounts/signup/', views.signup, name='signup'),
]

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

]

