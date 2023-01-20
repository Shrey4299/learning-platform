from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Room , Topic , Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout 
from django.contrib.auth.decorators import login_required
from django.http  import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# rooms = [
#     {'id' : 1 , 'name' : 'shrey' , 'company' : 'bigbasket'},
#     {'id' : 2 , 'name' : 'anurag' , 'company' : 'bigbasket'},
#     {'id' : 3 , 'name' : 'nikhil' , 'company' : 'google'}
# ]
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User not exist')   

        user = authenticate(request, username=username , password=password) 

        if user is not None:
            login(request,user)
            return redirect('home')

        else:
            messages.error(request, 'User or password  not exist')   
            
    context = {'page':page}
    return render(request, 'base/login_register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')

        else:
            messages.error(request, "An error has occured during the registration")
    return render(request, 'base/login_register.html',{'form': form})

def home(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q') 
    else:
        q = ''
    rooms = Room.objects.filter(
        Q( topic__name__icontains=q) |
        Q( name__icontains=q) |
        Q( description__icontains=q) 

       )

    topics = Topic.objects.all()
    room_count = rooms.count()


    context = {'rooms': rooms ,'topics' : topics ,'room_count' : room_count}
    return render(request, 'base/home.html', context)

def aboutus(request):
    return render(request, 'base/about.html')

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    
    context = {'room': room , 'room_messages' : room_messages ,'participants' : participants} 

    return render(request, 'base/room.html', context)

@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('you are not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('you are not allowed here')

    if request.method == 'POST':
       room.delete()
       return redirect('home')

    return render(request, 'base/delete.html', {'obj':room.name})


@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('you are not allowed here')

    if request.method == 'POST':
       message.delete()
       return redirect('home')

    return render(request, 'base/delete.html', {'obj':message})