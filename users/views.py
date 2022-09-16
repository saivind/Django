from multiprocessing import context
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CreateUserForm, LoginForm
from django.contrib import messages
from . import models
from django.contrib.auth.models import User
import MySQLdb as db
from MySQLdb import cursors
from MySQLdb import connect
from django.core.paginator import Paginator
from Files.models import Uploads, Req, Quality, Preprocess, ReqFiles

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from GUI_Interface.decorators import group_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
@group_required('superuser','manager')
#signup view
def SignupView(request):
    if request.method == "POST":
        print("in if")
        #process the form data
        form = CreateUserForm(request.POST)

        if form.is_valid():
            print("in if valid")
            
            #adding the user created to database
            user = form.save()
            group_manager = form.cleaned_data['is_manager'] 
            group_engineer = form.cleaned_data['is_engineer']

            user_email = form.cleaned_data['email']
            user = models.NewUser.objects.get(email=user_email)
            print("user_id",user)

            print('group_manager',group_manager)
            print('group_engineer',group_engineer)

            groups = Group.objects.all()
            print(groups)

            # user_groups = models.NewUser.groups()
            # print(user_groups)
            #  id | name     |
            # +----+----------+
            # |  2 | engineer |
            # |  1 | manager

            if group_manager == True:
                
                new_group = Group.objects.get(name = 'manager')
                #print(type(new_group))       # return tuple
                user.groups.add(new_group)
                
                
            if group_engineer == True:
                
                new_group = Group.objects.get(name = 'engineer')
                #print(type(new_group))       # return tuple
                user.groups.add(new_group)
                

            messages.success(request, 'User created successfully!')
            
            print("after login func")

            #validate the data
            # redirect a new URL
            files = Uploads.objects.count()
            num_req = ReqFiles.objects.count()
            num_users = models.NewUser.objects.count()
            context = {'files': files, 'no_req': num_req, 'no_user': num_users}
            return render(request, 'users/da.html',context)
        
    else:
        #create a blank form
        print("in get")
        form = CreateUserForm()

           
        # option1:
        # template = loader.get_template('createuser.html')
        # context = {'form': form,}
        # return HttpResponse(template.render(context, request))
    context = {'form':form}
    return render(request, 'users/createuser.html', context)

    
# #LogIn View
def LogInView(request):

    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        # #print("user details:", HttpRequest.readline)
        if form.is_valid():

            #user = form.get_user()
            email = request.POST.get('email')
            password = request.POST.get('password')
            print("in login if")
            print("user ", email, password)
            #print("pd ", password)
            user = authenticate(email=email, password=password) #authenticated the user
            if user is not None:

                print("in login when user is not none if")
                login(request, user) #logging in the user
                print("after login func")
                username = user.email
                #print(username)
                files = Uploads.objects.count()
                num_req = ReqFiles.objects.count()
                num_users = models.NewUser.objects.count()
                context = {'username1' : username,'files': files, 'no_req': num_req, 'no_user': num_users}
                
                return render(request, 'users/da.html',context)
            else:
                print("in login when user is  none if")
                messages.info(request, 'Email or Password is incorrect')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form}) # changed from login to index

@login_required
def LogOutUser(request):
    logout(request) #redirect to success page
    return render(request, 'home.html')

# def RemoveUser(request):
#     if request.method == 'POST':

@login_required
@group_required('superuser','manager')
def ListUsers(request):
    user_s = models.NewUser.objects.all()
    queryset = user_s
    p = Paginator(queryset,10)  # for 3 object per page
    #page_number = request.GET.get('page', 1)
    try:
        page_number = request.GET.get('page')
        
        page_object = p.page(page_number)
    except:
        page_object = p.page(1)
    context = {'users':user_s,
                'pages':page_object,}
    return render(request,"users/listuser.html",context)

@login_required    
@group_required('superuser','manager')
def delete(request):
    users = models.NewUser.objects.all()
    
    if request.method == 'POST':
        info = request.POST
        print(info)
        user_del = info['user_sel']
        print(user_del)
        record = models.NewUser.objects.get(email=user_del)
        record.delete()
        messages.success(request, 'User deleted successfully!')
        user_s = models.NewUser.objects.all()
        queryset = user_s
        p = Paginator(queryset,10)  # for 3 object per page
        #page_number = request.GET.get('page', 1)
        try:
            page_number = request.GET.get('page')
            
            page_object = p.page(page_number)
        except:
            page_object = p.page(1)
        context = {'users':user_s,
                    'pages':page_object,}
        return render(request,"users/delete.html",context)
    else:
        user_s = models.NewUser.objects.all()
        queryset = user_s
        p = Paginator(queryset,10)  # for 3 object per page
        #page_number = request.GET.get('page', 1)
        try:
            page_number = request.GET.get('page')
            
            page_object = p.page(page_number)
        except:
            page_object = p.page(1)
        context = {'users_all':user_s,
                    'pages':page_object,}
        return render(request,"users/delete.html",context)

@login_required
def dashboard(request):
    files = Uploads.objects.count()
    num_req = ReqFiles.objects.count()
    num_users = models.NewUser.objects.count()
    context = {'files': files, 'no_req': num_req, 'no_user': num_users}
    return render(request,"users/da.html", context)

def password_reset(request):
    if request.method == 'POST':
        info = request.POST
        print(info)
        
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})
    else:
        return render(request, "users/password_reset_form.html")
