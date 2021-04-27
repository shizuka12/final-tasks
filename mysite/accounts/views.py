from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')            
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/accounts/top')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form':form})


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('/accounts/top')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/signin.html', {'form':form})


def top(request):
    return HttpResponse('こちらはトップページ(仮)です。')
