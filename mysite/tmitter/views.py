from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TmeetForm
from .models import Tmeet
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from accounts.models import Follow
from django.contrib import messages

# Create your views here.
@login_required
def top(request):
    user = request.user
    timeline_userid_list = [ request.user.id ]
    following_list = Follow.objects.filter(follower__username=user.username)
    for follow in following_list:
        timeline_userid_list.append(follow.following.id)
    context = {
        'user': user,
        'tmeet_list': Tmeet.objects.all().order_by('-tmeeted_date'),
    }
    return render(request, 'tmitter/top.html', context)

@login_required
def accountpage(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {
        'user': user,
        'tmeet_list': Tmeet.objects.filter(author=user_id).order_by('-tmeeted_date'),
        'tmeet_num': Tmeet.objects.filter(author=user_id).count(),
        'following_num': Follow.objects.filter(follower__username=user.username).count(),
        'follower_num': Follow.objects.filter(following__username=user.username).count(),
        'already_followed': Follow.objects.filter(follower__username=request.user.username).filter(following__username=user.username),
    }
    return render(request, 'tmitter/accountpage.html', context)

@login_required
def tmeet(request):
    if request.method == "POST":
        form = TmeetForm(request.POST)
        if form.is_valid():
            tmeet = form.save(commit=False)
            tmeet.author = request.user
            tmeet.save()
            messages.success(request, 'ツミートしました')
            return redirect('tmitter:accountpage', request.user.id)
    else:
        form = TmeetForm()
    return render(request, 'tmitter/tmeet.html', {'form': form})

@login_required
def tmeet_detail(request, pk):
    tmeet = get_object_or_404(Tmeet, pk=pk)
    return render(request, 'tmitter/tmeet_detail.html', {'tmeet': tmeet})

@login_required
@require_POST
def delete_tmeet(request, pk):
    user = request.user
    tmeet = get_object_or_404(Tmeet, pk=pk)
    if user == tmeet.author:
        tmeet.delete()
    return redirect('tmitter:accountpage', request.user.id)
