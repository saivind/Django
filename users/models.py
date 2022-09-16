import email
from django.db import models
from django.utils.translation import gettext_lazy as _  
# from .managers import CustomUserManager  
from django.contrib.auth.models import AbstractUser, BaseUserManager

# # Create your models here.

class CustomAccountManager(BaseUserManager):
        
    def create_superuser(self,email,username,password,**other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_manager', True)
        other_fields.setdefault('is_engineer', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        print("values in superuser",self)
        return self.create_user(email, username, password, **other_fields)

    def create_user(self,email,username,password,**other_fields):
        if not email:
            raise ValueError(_("Users must have an email address"))
        if not username:
            raise ValueError(_("Users must have an unique username"))
        email=self.normalize_email(email)
        print("email",email)
        user=self.model(email=email,username=username)
        print("username",email+username)
        user.set_password(password)
        user.save()
    
    

class NewUser(AbstractUser):

    email            = models.EmailField(_('email address'), unique=True, max_length = 255) 
    username         = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    first_name       = models.CharField(max_length=60,blank=True)
    last_name        = models.CharField(max_length=30,blank=True)
    date_joined     = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superuser    = models.BooleanField('Is superuser', default=False)
    is_engineer     = models.BooleanField('Is engineer', default=False)
    is_manager      = models.BooleanField('Is manager', default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','username','is_superuser','is_manager','is_engineer','is_active','is_staff']

    def __str__(self):
        return self.email
