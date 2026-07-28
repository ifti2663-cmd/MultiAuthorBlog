from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import AuthorProfile
from .forms import PostForm
from .models import Post
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Comment, Like
def home(request):

    posts = Post.objects.filter(
        status="Published"
    ).order_by("-created_at")

    search = request.GET.get("search")

    if search:
        posts = posts.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search)
        )

    category = request.GET.get("category")

    if category:
        posts = posts.filter(category__id=category)

    tag = request.GET.get("tag")

    if tag:
        posts = posts.filter(tags__id=tag)

    paginator = Paginator(posts, 5)

    page = request.GET.get("page")

    posts = paginator.get_page(page)

    return render(
        request,
        "blog/home.html",
        {
            "posts": posts,
            "categories": Category.objects.all(),
            "tags": Tag.objects.all(),
        },
    )
def post_detail(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        status="Published"
    )

    session_key = f"viewed_{post.id}"

    if not request.session.get(session_key):
        Post.objects.filter(pk=post.pk).update(
            view_count=F("view_count") + 1
        )
        request.session[session_key] = True
        post.refresh_from_db()

    comments = post.comments.order_by("-created_at")

    liked = False

    if request.user.is_authenticated:
        liked = Like.objects.filter(
            user=request.user,
            post=post
        ).exists()

    context = {
        "post": post,
        "comments": comments,
        "liked": liked,
    }

    return render(
        request,
        "blog/post_detail.html",
        context,
    )
from django.contrib.auth.models import User
def author_profile(request, username):

    author = get_object_or_404(
        User,
        username=username
    )

    posts = Post.objects.filter(
        author=author,
        status="Published"
    )

    return render(
        request,
        "blog/author_profile.html",
        {
            "author": author,
            "posts": posts,
        },
    )
@login_required
def dashboard(request):

    profile = get_object_or_404(
        AuthorProfile,
        user=request.user
    )

    if not profile.is_author:
        return HttpResponseForbidden(
            "Only authors can access this page."
        )

    posts = Post.objects.filter(author=request.user)

    return render(
        request,
        "blog/dashboard.html",
        {"posts": posts},
    )


@login_required
def create_post(request):

    profile = get_object_or_404(
        AuthorProfile,
        user=request.user
    )

    if not profile.is_author:
        return HttpResponseForbidden(
            "Only authors can create posts."
        )

    if request.method == "POST":

        form = PostForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            post = form.save(commit=False)

            post.author = request.user

            post.save()

            form.save_m2m()

            return redirect("dashboard")

    else:

        form = PostForm()

    return render(
        request,
        "blog/post_form.html",
        {"form": form},
    )


@login_required
def edit_post(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return HttpResponseForbidden(
            "You cannot edit another author's post."
        )

    if request.method == "POST":

        form = PostForm(
            request.POST,
            request.FILES,
            instance=post,
        )

        if form.is_valid():

            form.save()

            return redirect("dashboard")

    else:

        form = PostForm(instance=post)

    return render(
        request,
        "blog/post_form.html",
        {"form": form},
    )


@login_required
def delete_post(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return HttpResponseForbidden(
            "You cannot delete another author's post."
        )

    if request.method == "POST":

        post.delete()

        return redirect("dashboard")

    return render(
        request,
        "blog/delete_post.html",
        {"post": post},
    )
@login_required
def add_comment(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        status="Published"
    )

    if request.method == "POST":

        text = request.POST.get("text")

        if text:

            Comment.objects.create(
                post=post,
                user=request.user,
                text=text,
            )

    return redirect("post_detail", slug=slug)
@login_required
def delete_comment(request, pk):

    comment = get_object_or_404(Comment, pk=pk)

    if (
        comment.user == request.user
        or comment.post.author == request.user
        or request.user.is_superuser
    ):

        slug = comment.post.slug

        comment.delete()

        return redirect("post_detail", slug=slug)

    return HttpResponseForbidden(
        "Permission denied."
    )
@login_required
def toggle_like(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        status="Published"
    )

    like = Like.objects.filter(
        user=request.user,
        post=post
    )

    if like.exists():

        like.delete()

    else:

        Like.objects.create(
            user=request.user,
            post=post,
        )

    return redirect(
        "post_detail",
        slug=slug,
    )