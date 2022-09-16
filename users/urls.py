
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views

app_name='users'

urlpatterns = [
    path('signup', views.SignupView, name='signup'),
    path('login', views.LogInView, name='login'),
    path('da', views.dashboard, name='da'),
    path('logout', views.LogOutUser, name='logout'),
    #path('admin', views.AdminView, name='admin'),
    path('listuser', views.ListUsers, name='listuser' ),
    path('password_reset_form', views.password_reset, name='password_reset_form' ),
    path('delete', views.delete, name='delete'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
