from django.shortcuts import render, redirect
from .models import Post,Comment
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User


# Create your views here.

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
            post = Post(
                image = form.cleaned_data["image"],
                title = form.cleaned_data["title"],
                image_caption = form.cleaned_data["image_caption"],
                author = request.user
            )
            
            post.save()

            post_name = form.cleaned_data.get('image_name')
            messages.success(request, f'Your post has been created for {post_name} !')
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


