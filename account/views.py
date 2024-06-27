from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import logout
from .forms import UserForm, ChangePasswordForm
from project.views import get_message_error

def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Log in the user
            login(request, user)
            return redirect('project-home')
        
        # Authentication failed
        error_message = 'Invalid username or password'
        messages.error(request, error_message)

    # GET request, display login form
    return render(request, 'login.html')

def log_out(request):
    logout(request)
    return redirect('login')  # Redirect to the desired page after logout (replace 'home' with your target URL name)

def update_profile(request):
    user = request.user
    if request.method == 'POST':
        userForm = UserForm(request.POST,instance=user)
        if userForm.is_valid():
            userForm.save()
            message = 'Profile updated successfully'
            return JsonResponse({'message':message})
    return render(request, 'profile.html', {'user': user})

def update_password(request):
    user = request.user
    if request.method == 'POST':
        passwordForm = ChangePasswordForm(request.POST,instance=user)
        if passwordForm.is_valid():
            passwordForm.save()
            message = 'Password updated successfully'
            return JsonResponse({'message':message})
        return JsonResponse({'message':get_message_error(passwordForm)})
    return render(request, 'profile.html', {'user': user})
