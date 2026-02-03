from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('verify-email/<str:token>/', views.verify_email, name='verify-email'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='user-profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
]
