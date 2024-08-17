from multiprocessing import context
from django.shortcuts import render, get_object_or_404, redirect
from blog_app.forms import PostForm, CommentForm
from blog_app.models import Post, Comment
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

# Create your views here.

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(username=username, password=password)

#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('blog_app:post_list'))
#             else:
#                 return HttpResponse('Account not found!')
#         else:
#             print('Someone tried to login and failed')
#             print('Username: {} and password {}'.format(username, password))
#             return HttpResponse('Invalid login details supplied')
#     else:
#         return render(request, 'registration/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("blog_app:post_list"))


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("blog_app:post_list"))
            else:
                return HttpResponse("Account not found!")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, "registration/login.html", {})


def register(request):
    error_message = None
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        if User.objects.filter(username=username).exists():
            error_message = "Username already exists"
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            user.save()
            messages.success(request, "Account created successfully")
            return redirect("user_login")
    return render(request, "registration/register.html", {"error_message": error_message})


class AboutView(TemplateView):
    template_name = "about.html"
    context_object_name = "about"


class PostListView(ListView):
    model = Post
    template_name = "blog_app/post_list.html"
    context_object_name = "post_list"

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by(
            "-published_date"
        )  # -published_date is to order the posts in descending order


class PostDetailView(DetailView):
    model = Post
    template_name = "blog_app/post_detail.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    redirect_field_name = "blog_app/post_list.html"
    form_class = PostForm
    model = Post
    template_name = "blog_app/post_form.html"
    context_object_name = "post"
    # fields = ['author', 'title', 'text']


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    redirect_field_name = "blog_app/post_detail.html"
    form_class = PostForm
    model = Post
    template_name = "blog_app/post_update.html"
    # fields = ['author', 'title', 'text']


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("blog_app:post_list")
    template_name = "blog_app/post_confirm_delete.html"
    content_object_name = "object"


class DraftListView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    template_name = "blog_app/draft_list.html"
    model = Post
    context_object_name = "draft_list"

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by("create_date")


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()

    return redirect("blog_app:post_detail", pk=pk)


# Comment views


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect("blog_app:post_detail", pk=post.pk)

    else:
        form = CommentForm()

    return render(request, "blog_app/comment_form.html", {"form": form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()

    return redirect("blog_app:post_detail", pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()

    return redirect("blog_app:post_detail", pk=post_pk)
