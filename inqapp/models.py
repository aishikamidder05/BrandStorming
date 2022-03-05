from django.db import models
from django.contrib.auth.models import User


class TeamDetail(models.Model):
    team = models.OneToOneField(User, on_delete= models.CASCADE, null=True)
    leader_name = models.CharField(blank=False, max_length=100)
    leader_email = models.EmailField(blank=False, max_length=80)
    leader_mobile = models.CharField(blank=False,max_length=10)
    member2_name = models.CharField(blank=True, max_length=100)
    member2_email = models.EmailField(blank=True, max_length=80)
    member3_name = models.CharField(blank=True, max_length=100)
    member3_email = models.EmailField(blank=True, max_length=80)
    isTeamAdded = models.BooleanField(default=False)
    isQuizTaken = models.BooleanField(default=False)
    isProductAllocated = models.BooleanField(default=False)
    product = models.CharField(max_length=500, blank=True, null=True )
    submission = models.CharField(max_length=500, blank=True, null=True)
    def __str__(self):
        return self.team.username
    
    def publish(self):
        self.save()


class Question(models.Model):
    question=models.CharField(max_length=500,blank=True)
    option1=models.ImageField(upload_to='images/',blank=True, null=True)
    option2=models.ImageField(upload_to='images/',blank=True, null=True)
    option3=models.ImageField(upload_to='images/',blank=True, null=True)
    option4=models.ImageField(upload_to='images/',blank=True, null=True)
    def publish(self):
        self.save()

    def __str__(self):
        return self.question


class Event(models.Model):
    Event_name=models.CharField(default="BrandStorming",max_length=50,blank=False)
    event_start=models.DateTimeField(auto_now_add=False)
    event_end=models.DateTimeField(auto_now_add=False)
