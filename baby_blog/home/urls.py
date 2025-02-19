from django.urls import path
from. views import *
from django.contrib.auth import views as auth_views
 
urlpatterns = [
    # path('', home, name='home'),
    path('register/', register, name='register'),
    # path('login/', auth_views.LoginView.as_view(template_name = 'engine/login.html'), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('', PostsListView.as_view(), name='home'),
    path('blog/<int:pk>/info/', PostDetailView.as_view(), name='blog-detail'),
    path('blog/create/', PostCreateView.as_view(), name='blog-create'),
    path('blog/<int:pk>/update/', PostUpdateView.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete/', PostDeleteView.as_view(), name='blog-delete'),
    path('<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('<str:username>/delete/', delete_user, name='delete-user'),
 
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'home/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name = "home/password_reset_done.html"), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'home/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'home/password_reset_complete.html'), name='password_reset_complete'),
]