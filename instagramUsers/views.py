from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,PostForm, CommentForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post,Comment,Profile
 

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

# def user_views (request):
#     post = Post.objects.all()
#     context = {
#         'post': post
#     }

#     return render (request, 'texts.html', context)

def home(request):
    post = Post.objects.all().order_by('-last_modified')

    context={
        'posts' : post,
    }

    return render(request, 'instagramHome/home.html',context)


def about(request):
    return render(request, 'instagramHome/about.html', {'title': 'About'})

@login_required
@csrf_protect
def add_post(request):
    form = PostForm(request.POST,request.FILES)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            # post = Post(
            #     image = form.cleaned_data["image"],
            #     image_name = form.cleaned_data["image_name"],
            #     image_caption = form.cleaned_data["image_caption"],
            #     author = request.user
            # )
            
            # post.save()

            # post_name = form.cleaned_data.get('image_name')
            form.save()
            messages.success(request, f'Your post has been created for {Post.author} !')
            return redirect('instagramHome-home')
    else:
        form = PostForm()

    return render(request, 'instagramHome/newPost.html',{'form': form})

@login_required
@csrf_protect
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author= user,
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()

    comments = Comment.objects.filter(post=post).order_by('-created_on')
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }

    return render(request, "instagramHome/post_detail.html", context)

@login_required
def like(request, pk):
    post = Post.objects.get(pk=pk)
    post.likes+=1
    post.save()
    return redirect('instagramHome-home')


