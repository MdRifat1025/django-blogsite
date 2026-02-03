from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Blog, Category, Rating, Favorite
from .forms import BlogForm, RatingForm, BlogSearchForm
from users.models import CustomUser


def blog_home(request):
    """Home page with list of all blogs with search and filtering"""
    
    blogs = Blog.objects.all()
    form = BlogSearchForm(request.GET)
    
    # Search by title or body
    search_query = request.GET.get('search')
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) | Q(body__icontains=search_query)
        )
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        blogs = blogs.filter(category_id=category)
    
    # Filter by author
    author = request.GET.get('author')
    if author:
        blogs = blogs.filter(author__username__icontains=author)
    
    # Sorting
    sort_by = request.GET.get('sort_by', 'date')
    if sort_by == 'date':
        blogs = blogs.order_by('-created_at')
    elif sort_by == '-date':
        blogs = blogs.order_by('created_at')
    elif sort_by == 'rating':
        # Sort by average rating
        blogs = sorted(blogs, key=lambda x: x.average_rating, reverse=True)
    elif sort_by == '-rating':
        blogs = sorted(blogs, key=lambda x: x.average_rating)
    elif sort_by == 'views':
        blogs = blogs.order_by('-views')
    
    # Pagination
    paginator = Paginator(blogs, 9)  # 9 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'blogs': page_obj,
        'form': form,
        'categories': Category.objects.all(),
    }
    
    return render(request, 'blogs/home.html', context)


def blog_detail(request, slug):
    """Display individual blog post with ratings"""
    
    blog = get_object_or_404(Blog, slug=slug)
    
    # Increment view count
    blog.views += 1
    blog.save(update_fields=['views'])
    
    # Get all ratings for this blog
    ratings = blog.ratings.all().order_by('-created_at')
    
    # Check if user has already rated
    user_rating = None
    is_favorited = False
    
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(blog=blog, user=request.user).first()
        is_favorited = Favorite.objects.filter(blog=blog, user=request.user).exists()
    
    context = {
        'blog': blog,
        'ratings': ratings,
        'user_rating': user_rating,
        'is_favorited': is_favorited,
        'average_rating': blog.average_rating,
        'rating_count': blog.rating_count,
    }
    
    return render(request, 'blogs/blog_detail.html', context)


@login_required
def blog_create(request):
    """Create a new blog post (Authors only)"""
    
    # Check if user is an author
    if request.user.role not in ['author', 'admin']:
        messages.error(request, 'Only authors can create blog posts.')
        return redirect('blog-home')
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Your blog has been created successfully!')
            return redirect('blog-detail', slug=blog.slug)
    else:
        form = BlogForm()
    
    return render(request, 'blogs/blog_form.html', {'form': form, 'title': 'Create Blog'})


@login_required
def blog_update(request, slug):
    """Update an existing blog post"""
    
    blog = get_object_or_404(Blog, slug=slug)
    
    # Check if user is the author or admin
    if blog.author != request.user and not request.user.is_staff:
        messages.error(request, 'You can only edit your own blog posts.')
        return redirect('blog-detail', slug=blog.slug)
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your blog has been updated successfully!')
            return redirect('blog-detail', slug=blog.slug)
    else:
        form = BlogForm(instance=blog)
    
    return render(request, 'blogs/blog_form.html', {
        'form': form,
        'title': 'Edit Blog',
        'blog': blog
    })


@login_required
def blog_delete(request, slug):
    """Delete a blog post"""
    
    blog = get_object_or_404(Blog, slug=slug)
    
    # Check if user is the author or admin
    if blog.author != request.user and not request.user.is_staff:
        messages.error(request, 'You can only delete your own blog posts.')
        return redirect('blog-detail', slug=blog.slug)
    
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Your blog has been deleted successfully!')
        return redirect('blog-home')
    
    return render(request, 'blogs/blog_confirm_delete.html', {'blog': blog})


@login_required
def rate_blog(request, slug):
    """Rate a blog post"""
    
    blog = get_object_or_404(Blog, slug=slug)
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            # Check if user has already rated
            existing_rating = Rating.objects.filter(blog=blog, user=request.user).first()
            
            if existing_rating:
                # Update existing rating
                existing_rating.rating = form.cleaned_data['rating']
                existing_rating.review = form.cleaned_data['review']
                existing_rating.save()
                messages.success(request, 'Your rating has been updated!')
            else:
                # Create new rating
                rating = form.save(commit=False)
                rating.blog = blog
                rating.user = request.user
                rating.save()
                messages.success(request, 'Thank you for rating this blog!')
            
            return redirect('blog-detail', slug=blog.slug)
    else:
        # Pre-fill form if user has already rated
        existing_rating = Rating.objects.filter(blog=blog, user=request.user).first()
        if existing_rating:
            form = RatingForm(instance=existing_rating)
        else:
            form = RatingForm()
    
    context = {
        'form': form,
        'blog': blog,
    }
    
    return render(request, 'blogs/rate_blog.html', context)


@login_required
def add_to_favorites(request, slug):
    """Add blog to user's favorites"""
    
    blog = get_object_or_404(Blog, slug=slug)
    
    # Check if already favorited
    favorite, created = Favorite.objects.get_or_create(user=request.user, blog=blog)
    
    if created:
        # Send email notification
        subject = f'{request.user.username} added your blog to favorites!'
        message = f'''
        Hello {blog.author.username},
        
        Good news! {request.user.username} has added your blog "{blog.title}" to their favorites.
        
        View your blog: {request.build_absolute_uri(blog.get_absolute_url())}
        
        Keep up the great work!
        
        Best regards,
        Blog Site Team
        '''
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [blog.author.email],
                fail_silently=True,
            )
        except Exception as e:
            pass  # Don't fail if email can't be sent
        
        messages.success(request, 'Blog added to your favorites!')
    else:
        messages.info(request, 'This blog is already in your favorites.')
    
    return redirect('blog-detail', slug=blog.slug)


@login_required
def remove_from_favorites(request, slug):
    """Remove blog from user's favorites"""
    
    blog = get_object_or_404(Blog, slug=slug)
    
    try:
        favorite = Favorite.objects.get(user=request.user, blog=blog)
        favorite.delete()
        messages.success(request, 'Blog removed from your favorites.')
    except Favorite.DoesNotExist:
        messages.error(request, 'This blog is not in your favorites.')
    
    return redirect('blog-detail', slug=blog.slug)


@login_required
def my_favorites(request):
    """Display user's favorite blogs"""
    
    favorites = Favorite.objects.filter(user=request.user).select_related('blog')
    
    # Pagination
    paginator = Paginator(favorites, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'favorites': page_obj,
    }
    
    return render(request, 'blogs/favorites.html', context)


def blogs_by_category(request, slug):
    """Display blogs filtered by category"""
    
    category = get_object_or_404(Category, slug=slug)
    blogs = Blog.objects.filter(category=category).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(blogs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'blogs': page_obj,
    }
    
    return render(request, 'blogs/category_blogs.html', context)


def author_blogs(request, username):
    """Display all blogs by a specific author"""
    
    author = get_object_or_404(CustomUser, username=username)
    blogs = Blog.objects.filter(author=author).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(blogs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'author': author,
        'blogs': page_obj,
    }
    
    return render(request, 'blogs/author_blogs.html', context)
