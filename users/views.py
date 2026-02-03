from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.crypto import get_random_string
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
from .models import CustomUser, Profile
from blogs.models import Blog


def register(request):
    """Handle user registration with email verification"""
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate until email verification
            
            # Generate email verification token
            token = get_random_string(length=64)
            user.email_verification_token = token
            user.save()
            
            # Create profile for the user
            Profile.objects.get_or_create(user=user)
            
            # Send verification email
            verification_url = request.build_absolute_uri(
                reverse('verify-email', args=[token])
            )
            
            subject = 'Verify your email address'
            message = f'''
            Hello {user.username},
            
            Thank you for registering at Blog Site!
            
            Please click the link below to verify your email address and activate your account:
            {verification_url}
            
            If you didn't create this account, please ignore this email.
            
            Best regards,
            Blog Site Team
            '''
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 
                    'Registration successful! Please check your email to verify your account.')
                return redirect('login')
            except Exception as e:
                messages.error(request, 
                    f'Registration successful but email could not be sent. Please contact support.')
                return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})


def verify_email(request, token):
    """Verify user email with token"""
    
    try:
        user = CustomUser.objects.get(email_verification_token=token)
        user.is_active = True
        user.is_email_verified = True
        user.email_verification_token = None
        user.save()
        
        messages.success(request, 
            'Your email has been verified successfully! You can now login.')
        return redirect('login')
    except CustomUser.DoesNotExist:
        messages.error(request, 
            'Invalid verification link. Please try again or contact support.')
        return redirect('register')


def user_login(request):
    """Handle user login"""
    
    if request.user.is_authenticated:
        return redirect('blog-home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, {username}!')
                    
                    # Redirect to next page if available
                    next_page = request.GET.get('next')
                    return redirect(next_page) if next_page else redirect('blog-home')
                else:
                    messages.error(request, 
                        'Your account is not activated. Please check your email for verification link.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})


@login_required
def user_logout(request):
    """Handle user logout"""
    
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('blog-home')


@login_required
def profile(request, username=None):
    """Display user profile"""
    
    if username:
        user = get_object_or_404(CustomUser, username=username)
    else:
        user = request.user
    
    profile_obj = user.profile
    
    # Get user's blogs if author
    if user.role == 'author':
        blogs = Blog.objects.filter(author=user).order_by('-created_at')
    else:
        blogs = None
    
    # Get user's favorites
    favorites = user.favorites.all()
    
    context = {
        'profile_user': user,
        'profile': profile_obj,
        'blogs': blogs,
        'favorites': favorites,
        'is_own_profile': request.user == user,
    }
    
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    
    return render(request, 'users/edit_profile.html', context)
