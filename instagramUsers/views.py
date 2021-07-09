from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from instagramHome.models import Post

# Create your views here.
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            for user in User.objects.all():
                 Profile.objects.get_or_create(user=user)

            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Accout has been created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'instagramUsers/register.html', {'form':form})

@login_required
@csrf_protect
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    user_posts = Post.objects.filter(author=request.user).order_by('-last_modified')
    post = Post.objects.filter(author=request.user).order_by('-last_modified')

    context = {
        'u_form' : u_form,
        'p_form' : p_form,
        'user_posts' : user_posts,
        'posts' : post
    }

    return render(request, 'instagramUsers/profile.html', context)