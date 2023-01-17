from django.db import models
import datetime
from django.contrib.auth import get_user_model


class Option(models.Model):
    options = models.CharField(default = 'option 1 unavailable', max_length=1000)
    votes = models.IntegerField(default = 0)
    percentage_vote = models.FloatField(default=0.0)
    color_code = models.CharField(max_length = 44, default ='green')
    def __str__(self):
        return self.options

class Room(models.Model):
    name = models.CharField(max_length=1000)
    topic = models.CharField(max_length=1000, default='this room deosnt have a topic up for discussion', null= True)
    opts = models.ManyToManyField(Option)
    total_votes = models.IntegerField(default = 0)
    user_count = models.IntegerField(default = 0)
    catagory = models.CharField(default= 'none', max_length=1000)
    time = models.DateTimeField(blank = True)
    pfp = models.ImageField(default='static/media/media/thisone.png')
    creator = models.CharField(default ='user not found', max_length=55)

    def __str__(self):
        return self.name

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profileimg = models.ImageField(upload_to='static/media/media/images', default='/media/static/media/media/thisone.png')
    rooms = models.ManyToManyField(Room)
    vote = models.ManyToManyField(Option)
    voted_rooms = models.ManyToManyField(Room,related_name= 'voted_room', blank=True)
    maximum_rooms = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

class Message(models.Model):
    value = models.CharField(max_length=10000)
    date = models.DateTimeField( blank=True)
    user = models.CharField(max_length=10000)
    room = models.CharField(max_length=10000)

class Catagories(models.Model):
    name = models.CharField(default = 'Anime', max_length=1000)
    profiles = models.ManyToManyField(Profile, blank=True)    
    def __str__(self):
        return self.name

class Saver(models.Model):
    name = models.CharField(default = 'yes', max_length= 100)
    saved = models.ManyToManyField(Option,blank=True )
    def __str__(self):
        return self.name