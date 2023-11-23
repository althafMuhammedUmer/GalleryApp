from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from app.views import index
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, UserProfile

from django.db import IntegrityError

# Create your views here.

def user_login(request):
    if request.user.is_authenticated:
        return redirect(index)
    else:
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(request, email=email, password=password)

            if user is not None :

                login(request, user)
                return redirect(index)
            else:      
                messages.error(request, "Invalid login credentials")
    
        return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        
        if password == confirm_password:
            try:
                user = CustomUser.objects.create(
                    username=username,
                    email=email,
                    password=password,
                )
                user.save()
                login(request, user)
                return redirect(index)
            
            except IntegrityError as e:
                messages.error(request, 'Email address is already in use.')
                
            except Exception as e:
                messages.error(request, f'Error during registration: {str(e)}')
        
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'register.html')


@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    return redirect(user_login)


def get_user_details(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email,
        "bio": user.userprofile.bio,
    }

    return JsonResponse({"data": data})
