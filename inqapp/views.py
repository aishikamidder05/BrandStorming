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
import random
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
            return redirect('signin')
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
       return redirect('signin')
    if TeamDetail.objects.filter(team=request.user).exists():
        questions = Question.objects.all()
        team = TeamDetail.objects.get(team=request.user)
        return render(request,'question.html', {'questions':questions, 'team':team})
    else:
        return redirect('home')

def contact(request):
    return render(request,'contact.html')

product_list = [
    "Flying car: car which can fly",
    "Smart glass: goggles that can store information and can display things",
    "Smart brush:  toothbrush that is automatic and adjusts itself with respect to age, remind user to brush in time",
    "Flying surfboard: can surf on air",
    "Flying broom: broom that can be used in 'Quidditch'",
    "Wireless charger: can charge any electronic device from a distance without wire",
    "Smart water bottle:  bottle that can inform about any liquid inside it and purify or change temp. accordingly",
    "Smart bed: adjusts itself with the sleeping posture and helps to make the correct",
    "Flying saucer: object to travel in space",
    "Smart pen : store information and record things also",
    "Mobile Music: Carry your favorite playlist on your wrist.",
    "Garden online: Transmit plant’s data to your computer so that you can see just what your plant needs.",
    "Cloud Sofa: Floating sofa- Bring heaven home",
    "The Neuralizer:  this gadget lets you zap away the memories of those who stare at the flashing red light",
    "The Lightsaber: an elegant weapon from a more civilized age",
    "The Electronic Thumb: hitch a ride with an alien",
    "Portable Lamp: Lamp that can also be carried like a torch",
    "PC Projector: Computer, keyboard, and projector all in one device.",
    "Hologram shield: A shield which is simply a frame and uses a hologram to protect",
    "Smart torch : torch with light regulator", 
    "Mr. Fusion- generate all our power needs just by feeding in some garbage.",
    "Iron Mans Armor- It can fly, it's impervious to most forms of damage and it features repulsor beams that can blast holes in masonry",
    "Time Machine- Hop into your handy-dandy time machine and risk introducing a paradox that could rip apart the very fabric of time and space in order to prevent yourself from an embarrassing situation",
    "The Transporter- The device that could dematerialize you, shoot you across vast distances and reassemble you at your destination",
    "The Replicator-  It can create stuff as long as it knows what that stuff is made of on a molecular level",
    "The Sonic Screwdriver- It can open (or engage) locks ranging from rusty old padlocks to digital keypads. It can reprogram computers and repair old wiring. In a pinch, you can use it as a weapon and knock people unconscious with it or pair it with a power source to zap Daleks or Cybermen",
    "Anywhere door: can go anywhere by opening the door",
    "Spyglass: Binoculars that can see through opaque objects",
    "3D Projector: Design on a drawing book and project a 3D image",
    "Catch Gloves: Gloves that makes sure you always catch the ball"
]

def productAllot(request):
    if request.user.is_anonymous:
       return redirect('signin')
    if TeamDetail.objects.filter(team=request.user).exists():
        index = random.randint(0,29)
        team = TeamDetail.objects.get(team=request.user)
        team.product = product_list[index]
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