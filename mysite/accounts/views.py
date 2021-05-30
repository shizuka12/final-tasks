from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Follow
from django.contrib import messages

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
            return redirect('tmitter:top')
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
            return redirect('tmitter:top')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/signin.html', {'form':form})


@require_POST
def signout(request):
    logout(request)
    return redirect('accounts:signin')


@login_required
def follow(request, user_id):
    follower = request.user
    following = get_object_or_404(User, pk=user_id)

    if follower == following:
        messages.warning(request, '自分をフォローすることはできません')
    else:
        follow, created = Follow.objects.get_or_create(follower=follower, following=following)
        if (created):
            messages.success(request, following.username + 'をフォローしました')
        else:
            messages.warning(request, 'あなたはすでに' + following.username + 'をフォローしています')
    
    return redirect('tmitter:accountpage', user_id)


@login_required
def unfollow(request, user_id):
    follower = request.user
    following = get_object_or_404(User, pk=user_id)

    if follower == following:
        messages.warning(request, '無効な操作です')
    else:
        unfollow = Follow.objects.get(follower=follower, following=following)
        unfollow.delete()
        messages.success(request, following.username + 'のフォローを解除しました')

    return redirect('tmitter:accountpage', user_id)


@login_required
def following_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {
        'user': user,
        'following_list': Follow.objects.filter(follower__username=user.username).order_by('-followed_date'),
    }
    return render(request, 'accounts/following_detail.html', context)


@login_required
def follower_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {
        'user': user,
        'follower_list': Follow.objects.filter(following__username=user.username).order_by('-followed_date'),
    }
    return render(request, 'accounts/follower_detail.html', context)
