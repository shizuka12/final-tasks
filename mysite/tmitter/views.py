from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TmeetForm
from .models import Tmeet
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

# Create your views here.
@login_required
def top(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {
        'user': user,
        'tmeet_list': Tmeet.objects.all().order_by('-created_at'),
    }
    return render(request, 'tmitter/top.html', context)

@login_required
def accountpage(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {
        'user': user,
        'tmeet_list': Tmeet.objects.filter(author=user_id).order_by('-created_at'),
    }
    return render(request, 'tmitter/accountpage.html', context)

@login_required
def tmeet(request, user_id):
    if request.method == "POST":
        form = TmeetForm(request.POST)
        if form.is_valid():
            tmeet = form.save(commit=False)
            tmeet.author = request.user
            tmeet.save()
            return redirect('tmitter:accountpage', request.user.id)
    else:
        form = TmeetForm()
    return render(request, 'tmitter/tmeet.html', {'form': form})

@login_required
def tmeet_detail(request, user_id, pk):
    user = get_object_or_404(User, pk=user_id)
    tmeet = get_object_or_404(Tmeet, pk=pk)
    return render(request, 'tmitter/tmeet_detail.html', {'tmeet': tmeet})

@login_required
@require_POST
def delete_tmeet(request, user_id, pk):
    user = get_object_or_404(User, pk=user_id)
    tmeet = get_object_or_404(Tmeet, pk=pk)
    tmeet.delete()
    return redirect('tmitter:accountpage', request.user.id)
