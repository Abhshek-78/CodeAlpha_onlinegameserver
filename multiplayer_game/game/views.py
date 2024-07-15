from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def find_match(request):
    player = get_object_or_404(Player, user=request.user)
    available_games = Game.objects.filter(player2__isnull=True).exclude(player1=player)
    if available_games.exists():
        game = available_games.first()
        game.player2 = player
        game.save()
    else:
        game = Game.objects.create(player1=player)
    return JsonResponse({'game_id': game.id})

from django.shortcuts import render

def game_room(request, room_name):
    return render(request, 'game.html', {
        'room_name': room_name
    })
