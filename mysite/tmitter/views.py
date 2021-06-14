from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TmeetForm
from .models import Tmeet, Favorite
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from accounts.models import Follow
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse

# Create your views here.
@login_required
def top(request):
    user = request.user
    context = {
        'user': user,
        'tmeet_list': Tmeet.objects.select_related('author').all().order_by('-tmeeted_date'),
    }
    return render(request, 'tmitter/top.html', context)

@login_required
def accountpage(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {
        'user': user,
        'tmeet_list': Tmeet.objects.filter(author=user_id).order_by('-tmeeted_date'),
        'tmeet_num': Tmeet.objects.filter(author=user_id).count(),
        'following_num': user.follower.count(),
        'follower_num': user.following.count(),
        'is_following': Follow.objects.filter(follower__username=request.user.username, following__username=user.username).exists(),
        'account_fav_num': Favorite.objects.filter(fav_user=user_id).count(),
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
    context = {
        'tmeet': tmeet,
        'fav_num': Favorite.objects.filter(tmeet=tmeet).count(),
        'is_favoriting': Favorite.objects.filter(tmeet=tmeet, fav_user=request.user).exists(),
    }
    return render(request, 'tmitter/tmeet_detail.html', context)

@login_required
@require_POST
def delete_tmeet(request, pk):
    user = request.user
    tmeet = get_object_or_404(Tmeet, pk=pk)
    if user == tmeet.author:
        tmeet.delete()
    return redirect('tmitter:accountpage', request.user.id)


@login_required
@require_POST
def favorite(request):
    pk = request.POST["pk"]
    fav_user = request.user
    tmeet = get_object_or_404(Tmeet, pk=pk)
    favorite, created = Favorite.objects.get_or_create(fav_user=fav_user, tmeet=tmeet)
    if not (created):
        favorite.delete()
    fav_num = Favorite.objects.filter(tmeet=tmeet).count()
    data = {
        'fav_num': f'{fav_num} お気に入り' if fav_num != 0 else '',
        'button': 'お気に入り解除' if created else 'お気に入り'
    }
    return JsonResponse(data)


@login_required
def tmeet_fav_detail(request, pk):
    context = {
        'pk':pk,
        'fav_user_list': Favorite.objects.filter(tmeet__pk=pk).select_related('fav_user').order_by('fav_date')
        }
    return render(request, 'tmitter/tmeet_fav_detail.html', context)


@login_required
def account_fav_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    pk_list = Favorite.objects.filter(fav_user=user).values_list('tmeet__pk', flat=True)
    pk_list = list(pk_list)
    context = {
        'user': user,
        'fav_list': Tmeet.objects.filter(pk__in=pk_list).select_related('author'),
        'tmeet_num': Tmeet.objects.filter(author=user_id).count(),
        'following_num': user.follower.count(),
        'follower_num': user.following.count(),
        'is_following': Follow.objects.filter(follower__username=request.user.username, following__username=user.username).exists(),
        'account_fav_num': Favorite.objects.filter(fav_user=user_id).count(),
        }
    return render(request, 'tmitter/account_fav_detail.html', context)
