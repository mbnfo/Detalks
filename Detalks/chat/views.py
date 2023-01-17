from django.shortcuts import render, redirect
from chat.models import Catagories, Room, Message, Profile,Option,Saver
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random
import datetime
import pytz

timezone = pytz.timezone('US/Central')
expired = []
# Create your views here.

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        opt = Saver.objects.all()

        if password == password1:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signin')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signin')
            else:
                createuser = User.objects.create_user(username=username, email=email, password=password)
                createuser.save()

                
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id=user_model.id)
                new_profile.save()
                opt = Saver.objects.create(name=username)
                opt.save()
                return redirect('settings_signin')     
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signin')
        
    return render(request, 'signin.html')

def settings_signin(request):
    category = Catagories.objects.all()
    return render(request, 'settings_signin.html', {
        'category':category
        })

def login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('login')

    else:
        return render(request, 'login.html')

def settings(request):
    category = Catagories.objects.all()
    user = Profile.objects.get(user = request.user.id)
    if request.method =='POST':
        if request.FILES.get('image') == None:
            image = user.profileimg
            user.profileimg = image
            user.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            user.profileimg = image
            user.save()
        
    if request.method == 'POST':
            choice0 = request.POST['choice0']
            choice1 = request.POST['choice1']
            choice2 = request.POST['choice2']

            cat0 = Catagories.objects.get(name= choice0)
            cat1 = Catagories.objects.get(name= choice1)
            cat2 = Catagories.objects.get(name= choice2)

            cat0.profiles.add(user)
            cat1.profiles.add(user)
            cat2.profiles.add(user)
            return redirect('/')
    return render(request, 'settings.html',{
        'user':user,
        'category':category,
    })
def describer(request):
    return render(request,'describer.html')

@login_required(login_url='login')
def home(request):
    user = Profile.objects.get(user = request.user.id)
    room = Room.objects.all()
    for i in user.rooms.all():
        if i in expired:
            i.delete()
    return render(request, 'Home.html', {
        'room':room,
        'user':user,
    })

@login_required(login_url='login')
def room(request, room):
    username = Profile.objects.get(user = request.user.id)
    room_details = Room.objects.get(name=room)
    
    if request.method == 'POST':
        inputvalue = request.POST['choice']
        selected = Option.objects.get(id = inputvalue)
        
        if Profile.objects.filter(id = username.id,voted_rooms = room_details.id).exists():
            messages.info(request,'you have aready voted' )
            pass
        else:
            selected.votes += 1
            selected.save()
            room_details.total_votes += 1
            for i in room_details.opts.all():
                i.percentage_vote = i.votes / room_details.total_votes * 100
                i.save()
                Room.objects.update()
                Option.objects.update()
            username.voted_rooms.add(room_details)
            room_details.save()
            username.save()
            Room.objects.update()
            return redirect('/'+room_details.name)
    

    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details,
        })
            
def send(request):
    username = User.objects.get(username=request.user.username)
    msg = request.POST['message']
    room_id = request.POST['room_id']
    chatroom = Room.objects.get(id = room_id)
    if datetime.datetime.now(timezone) > chatroom.time + datetime.timedelta(hours=24):
            new_message = Message.objects.create(value='This chatroom has expired and no new messages can be sent. please kindly redirect to the home page and pick another chatroom to communicate in and thank you for visiting our site!', user='system', room=room_id, date = datetime.datetime.now(timezone))
            new_message.save()
            expired.append(chatroom)
    else:
        new_message = Message.objects.create(value=msg, user=username.username, room=room_id, date = datetime.datetime.now(timezone))
        new_message.save()



    
@login_required(login_url='login')
def create_room(request):
    #options adder
    user = Profile.objects.get(user = request.user.id)
    opt = Saver.objects.get(name=user)
    catagories = Catagories.objects.all()
    return render(request, 'create_room.html', {
        'opt':opt,
        'catagories':catagories,
        'user':user,
    }) 

def addoption(request):
    if request.method == 'POST':
        user = Profile.objects.get(user = request.user.id)
        opt = Saver.objects.get(name=user)
        option = request.POST['option']
        opts = Option.objects.create(options=option)
        opt.saved.add(opts)
        opt.save()
        return redirect('/create_room')
    return render(request, 'addoption.html')
       
@login_required(login_url='login')
def checkview(request):
    #variables for room creation
    room = request.POST['room_name']
    user = Profile.objects.get(user = request.user.id)
    discussion = request.POST['topic']
    catagori = request.POST['choice']
    opts = Saver.objects.get(name=user)
    
#to check if the room exists, if the room exists then just say the room exists,if not create it
    if Room.objects.filter(name=room).exists():
        messages.info(request, 'this room aleady exists')
        return redirect('/create_room')
    else:
        new_room = Room.objects.create(name=room,topic=discussion, user_count = 1,time = datetime.datetime.now(timezone),catagory = catagori,pfp = user.profileimg, creator = str(user) )
        new_room.save()
        new_room.time = datetime.datetime.now(timezone)
        user.rooms.add(new_room)
        if opts.saved.all is not None:
            for i in opts.saved.all():
                new_room.opts.add(i)
                opts.saved.remove(i)
    addUser(new_room,catagori)
    return redirect('/' + str(room))


def addUser(room, catagory):
    user_object = User.objects.all()
    candidate = Catagories.objects.get(name = catagory)
    use = []
    try:
        for i in candidate.profiles.all():
            user = Profile.objects.get(user = user_object.get(profile = i))
            use.append(user)

        while room.user_count < 10:
            random_user = random.choice(use)
            adding_user = Profile.objects.get(user = user_object.get(profile = random_user))
            if adding_user.maximum_rooms < 8:
                adding_user.rooms.add(room)
                use.remove(adding_user)
                room.user_count += 1
            else:
                use.remove(random_user)
    except :
        'list index out of range'
        
    return redirect('/' + str(room))


def getMessages(request, room):
    chatroom = Room.objects.get(name=room)
    messages = Message.objects.filter(room=chatroom.id)
    return JsonResponse({"messages":list(messages.values())})
            
