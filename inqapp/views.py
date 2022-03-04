from django.shortcuts import render
from .models import Question , Event, TeamDetail
from .forms import TeamForm
from django.contrib.auth.decorators import login_required
from django.views import  View
from django.shortcuts import render, get_object_or_404,render
from django.shortcuts import redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
import datetime
import requests
from django.utils.timezone import utc

def home(request):
    if request.user.is_anonymous:
       return render(request,'welcome.html',{})
    else: 
        if TeamDetail.objects.filter(team=request.user).exists():
            team = TeamDetail.objects.get(team=request.user)
            return render(request,'welcome.html',{"team":team})
        return render(request,'welcome.html',{'team': 'none'})

class TeamDetailView(View):
    def get(self, request):
        if self.request.user.is_anonymous:
            return redirect('home')
        else:
            if TeamDetail.objects.filter(team=request.user).exists():
                team = TeamDetail.objects.get(team=request.user)
                return render(request, 'teamDetail.html', {'team': team, 'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})
            return render(request, 'teamDetail.html', {'team': 'none', 'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})

    def post(self, request):
        form =TeamForm(request.POST)

        recaptcha_response = request.POST['g-recaptcha-response']
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        print(result)

        if result['success']:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.team = self.request.user
                instance.isTeamAdded = True
                instance.save()
                team = TeamDetail.objects.get(team=request.user)
                message = "Team updated successfully"
                return render(request, 'teamDetail.html', {'message': message, 'team': team, 'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})
            
            else:
                message = "Could not update. Please try again."
                return render(request, 'teamDetail.html', {'message': message, 'team':'none', 'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})

        else:
            message = "Could not update. Please try again."
            return render(request, 'teamDetail.html', {'message': message, 'team':'none', 'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})
                

def question(request):
    if request.user.is_anonymous:
       return redirect('home')
    if TeamDetail.objects.filter(team=request.user).exists():
        questions = Question.objects.all()
        team = TeamDetail.objects.get(team=request.user)
        return render(request,'question.html', {'questions':questions, 'team':team})
    else:
        return redirect('home')

def contact(request):
    return render(request,'contact.html')

def productAllot(request):
    if request.user.is_anonymous:
       return redirect('home')
    if TeamDetail.objects.filter(team=request.user).exists():
        team = TeamDetail.objects.get(team=request.user)
        team.product = "test"
        team.isProductAllocated = True
        team.save()
        return redirect('home')
    else:
        return redirect('home')

def noPage(request):
    return render(request,'404.html')

class RegistrationView(View):
    def get(self, request):
        return render(request, 'signup.html', {'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})

    def post(self, request):

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        recaptcha_response = request.POST['g-recaptcha-response']
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        print(result)

        if result['success']:
            if username and email and password:
                if not User.objects.filter(username=username).exists():
                    if not User.objects.filter(email=email).exists():
                        if len(password) < 6:
                            message = 'Password too short'
                            return render(request, 'signup.html', {'message':message,'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})

                        user = User.objects.create_user(username=username, email=email)
                        user.set_password(password)
                        user.save()
                        message = "Account successfully created"
                        return render(request, 'registration/login.html', {'message':message, 'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})
                
                message = 'User already exists'
                return render(request,  'signup.html', {'message':message, 'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})
            message = 'Fill all the Fields'
            return render(request, 'signup.html', {'message':message, 'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})

        message = 'Could not register. Please try again'
        return render(request, 'signup.html', {'message':message, 'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})
        


class LoginView(View):
    def get(self, request):
        return render(request,'registration/login.html',{'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        recaptcha_response = request.POST['g-recaptcha-response']
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        print(result)

        if result['success']:

            if username and password:
                user = authenticate(username=username, password=password)

                if user:
                    login(request, user)
                    return redirect('home')

                message = 'Invalid Credentials'
                return render(request, 'registration/login.html', {'message':message, 'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})

            message = 'Fill all the fields'
            return render(request, 'registration/login.html', {'message':message, 'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})

        message = 'Could not login. Please try again'
        return render(request, 'registration/login.html', {'message':message, 'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')