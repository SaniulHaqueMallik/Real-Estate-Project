from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth  # Import the auth module


# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'User already Exists')
                return redirect(register)
            else:
                if User.objects.filter(email=email):
                    messages.error(request, 'Email already registered')
                    return redirect(register)
                else:
                    user =  User.objects.create(first_name = first_name, last_name = last_name,
                    username= username, password= password)
                    user.save()
                    messages.success(request, 'You are now logged in')
                    return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect(register)
        
    else:
        # If it's not a POST request, render the registration form
        return render(request, 'accounts/register.html')  # Adjust the template name as needed

def login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,'You are logged in')
            return redirect('dashboard')
        
        messages.error(request, 'Invalid Credentials')
        return redirect(login)
        
    
    return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
     
        return redirect('index')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')