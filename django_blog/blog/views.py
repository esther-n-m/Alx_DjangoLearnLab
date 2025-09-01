from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect , get_object_or_404

from .forms import RegisterForm, ProfileForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.db.models import Q
from .models import Post, Tag



def register(request):
    """User registration using a custom form that includes email."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully. You’re now logged in.")
            login(request, user)  # auto-login after registration
            return redirect("profile")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
    """View + edit profile (first name, last name, email)."""
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "blog/profile.html", {"form": form})


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"       # GET /posts/
    context_object_name = "posts"
    ordering = ["-published_date"]              # newest first
    paginate_by = 10                            # optional


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"     # GET /posts/<pk>/
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_form.html"       # GET/POST /posts/new/
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/post_form.html"       # GET/POST /posts/<pk>/edit/
    form_class = PostForm

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"   # GET/POST /posts/<pk>/delete/
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comment_form"] = CommentForm()
        ctx["comments"] = self.object.comments.select_related("author")
        return ctx

    def post(self, request, *args, **kwargs):
        """
        Handle inline comment creation on the post detail page.
        Only for authenticated users.
        """
        self.object = self.get_object()
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to comment.")
            return redirect("login")

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment posted.")
            return redirect("post-detail", pk=self.object.pk)

        # If invalid, re-render page with errors
        ctx = self.get_context_data()
        ctx["comment_form"] = form
        return self.render_to_response(ctx)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post_id})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post_id})
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"  # you can reuse the same template

    def form_valid(self, form):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})
    
def search_posts(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    return render(request, 'blog/search_results.html', {'results': results, 'query': query})

def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = tag.posts.all()
    return render(request, 'blog/posts_by_tag.html', {'tag': tag, 'posts': posts})