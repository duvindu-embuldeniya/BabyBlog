from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from . forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . models import Posts
from django.urls import reverse_lazy
from django.http import HttpResponse

class PostsListView(ListView):
    model = Posts
    template_name = 'home/index.html'
    context_object_name = 'posts'
    ordering = ['date_posted'] 
    paginate_by = 2

class PostDetailView(DetailView):
    model = Posts
    template_name = 'home/detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Posts
    template_name = 'home/create.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    template_name = 'home/update.html'
    fields = ['title', 'content']
    
    def test_func(self):
        post = self.get_object()
        if post.author != self.request.user:
            return False
        return True
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    template_name = 'home/delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        if post.author != self.request.user:
            return False
        return True

class UserPostListView(ListView):
    model = Posts
    template_name = 'home/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Posts.objects.filter(author=user).order_by('date_posted')

@login_required
def delete_user(request, username):
    object = User.objects.get(username=username)
    if object != request.user:
        return HttpResponse("<h1>403 Forbidden</h1>")
    if request.method == 'POST':
        object.delete()
        messages.success(request, f"Account has been deleted successfully!")
        return redirect('home')
    else:
        return render(request, 'home/profile_delete.html', {'object': object})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            auth.login(request, new_user)
            messages.success(request, f"Your Account has been Created!")
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'home/register.html', {'form': form})

class CustomLoginView(auth_views.LoginView):
    template_name = 'home/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in!")
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "You have logged in successfully!")
        return super().get_success_url()
    
def logout(request):
    if not(request.user.is_authenticated):
        messages.info(request, f"You haven't logged in!")
        return redirect('home')
    auth.logout(request)
    messages.success(request, "You have logged out successfully!")
    return render(request, 'home/logout.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile updated successfully!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)
    return render(request, 'home/profile.html', {'u_form':u_form, 'p_form':p_form})
