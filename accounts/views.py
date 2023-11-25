from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from app.views import index
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, UserProfile, OTP
from django.core.serializers import serialize
from decouple import config
from twilio.rest import Client

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

@login_required(login_url='user_login')
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

@login_required(login_url='user_login')
def update_user_profile(request, user_id):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    bio = request.POST.get('bio')
    image = request.FILES.get('image')

    user = get_object_or_404(CustomUser, pk=user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.username = username
    user.email = email
    user.save()

    userprofile = get_object_or_404(UserProfile, user=user)

    userprofile.profile_picture =  image if request.FILES.get('image') else userprofile.profile_picture
    userprofile.bio = bio
    userprofile.save()

    
    return JsonResponse({"data": True})


def forgot_password(request):
    return render(request, 'forgotpassword.html')


def check_email_isExist(request, email_id):
    if request.method == "GET":
        
        email_exist = CustomUser.objects.filter(email=email_id).exists()

        return JsonResponse({"exists": email_exist})
    
    return JsonResponse({"exists": False})

def generate_otp(request):
    if request.method == "POST":
        user_contact = request.POST.get('user_contact')

        otp = OTP.generate_otp(user_contact)

        try:
            TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
            TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
            TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER')

            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            message = client.messages.create(
                body=f"Your OTP is {otp}",
                from_=TWILIO_PHONE_NUMBER,
                to=user_contact
            )

            print(message.sid)

            return JsonResponse({'otp send': True})
        
        except Exception as e:
            return JsonResponse({'error': str(e)})
        
    
    return JsonResponse({'error': "Invalid request."})


