"""
Setup script to initialize the blog site with sample data
Run this after migrations: python setup_sample_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from users.models import CustomUser, Profile
from blogs.models import Blog, Category
from django.utils.text import slugify


def create_categories():
    """Create sample categories"""
    categories = [
        {'name': 'Technology', 'description': 'All about technology and innovation'},
        {'name': 'Travel', 'description': 'Travel stories and destination guides'},
        {'name': 'Food', 'description': 'Recipes, restaurants, and culinary adventures'},
        {'name': 'Lifestyle', 'description': 'Health, wellness, and lifestyle tips'},
        {'name': 'Business', 'description': 'Business insights and entrepreneurship'},
        {'name': 'Education', 'description': 'Learning and educational content'},
    ]
    
    for cat in categories:
        Category.objects.get_or_create(
            name=cat['name'],
            defaults={'slug': slugify(cat['name']), 'description': cat['description']}
        )
    print(f"✓ Created {len(categories)} categories")


def create_sample_users():
    """Create sample users"""
    # Create admin
    if not CustomUser.objects.filter(username='admin').exists():
        admin = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@blogsite.com',
            password='admin123',
            role='admin'
        )
        admin.is_email_verified = True
        admin.save()
        print("✓ Created admin user (username: admin, password: admin123)")
    
    # Create authors
    authors_data = [
        {'username': 'john_author', 'email': 'john@example.com', 'bio': 'Tech enthusiast and blogger'},
        {'username': 'jane_writer', 'email': 'jane@example.com', 'bio': 'Travel lover sharing adventures'},
    ]
    
    for author_data in authors_data:
        if not CustomUser.objects.filter(username=author_data['username']).exists():
            user = CustomUser.objects.create_user(
                username=author_data['username'],
                email=author_data['email'],
                password='password123',
                role='author'
            )
            user.is_email_verified = True
            user.is_active = True
            user.save()
            
            # Update profile bio
            profile = Profile.objects.get(user=user)
            profile.bio = author_data['bio']
            profile.save()
            
            print(f"✓ Created author: {author_data['username']} (password: password123)")
    
    # Create readers
    if not CustomUser.objects.filter(username='reader').exists():
        reader = CustomUser.objects.create_user(
            username='reader',
            email='reader@example.com',
            password='password123',
            role='reader'
        )
        reader.is_email_verified = True
        reader.is_active = True
        reader.save()
        print("✓ Created reader user (username: reader, password: password123)")


def create_sample_blogs():
    """Create sample blog posts"""
    tech_cat = Category.objects.get(name='Technology')
    travel_cat = Category.objects.get(name='Travel')
    
    author = CustomUser.objects.get(username='john_author')
    
    sample_blogs = [
        {
            'title': 'Getting Started with Python Django',
            'body': '''Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. 
            
            In this guide, we'll explore the fundamentals of Django and how to build your first web application.
            
            Django follows the Model-View-Template (MVT) architectural pattern, which is similar to MVC but with some key differences.
            
            Key Features of Django:
            - Object-Relational Mapping (ORM)
            - Admin Interface
            - URL Routing
            - Template Engine
            - Security Features
            
            Let's dive into creating your first Django project and understand how all these components work together!''',
            'category': tech_cat,
            'author': author,
        },
        {
            'title': 'Top 10 Travel Destinations for 2024',
            'body': '''Planning your next adventure? Here are the top 10 destinations you should consider visiting in 2024.
            
            1. Japan - Experience cherry blossoms and rich culture
            2. Iceland - Natural wonders and northern lights
            3. New Zealand - Adventure sports and stunning landscapes
            4. Portugal - Historic cities and beautiful coastlines
            5. Morocco - Exotic markets and desert adventures
            
            Each destination offers unique experiences and memories that will last a lifetime!''',
            'category': travel_cat,
            'author': author,
        },
    ]
    
    created_count = 0
    for blog_data in sample_blogs:
        if not Blog.objects.filter(title=blog_data['title']).exists():
            Blog.objects.create(**blog_data)
            created_count += 1
    
    print(f"✓ Created {created_count} sample blog posts")


def main():
    """Run all setup functions"""
    print("\n" + "="*50)
    print("Setting up Blog Site with sample data...")
    print("="*50 + "\n")
    
    create_categories()
    create_sample_users()
    create_sample_blogs()
    
    print("\n" + "="*50)
    print("Setup completed successfully!")
    print("="*50)
    print("\nYou can now login with:")
    print("  Admin: username=admin, password=admin123")
    print("  Author: username=john_author, password=password123")
    print("  Reader: username=reader, password=password123")
    print("\n")


if __name__ == '__main__':
    main()
