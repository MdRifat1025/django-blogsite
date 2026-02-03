from django.contrib import admin
from .models import Blog, Category, Rating, Favorite


class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category model"""
    
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


class BlogAdmin(admin.ModelAdmin):
    """Admin for Blog model"""
    
    list_display = ['title', 'author', 'category', 'created_at', 'views']
    list_filter = ['category', 'created_at', 'author']
    search_fields = ['title', 'body', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


class RatingAdmin(admin.ModelAdmin):
    """Admin for Rating model"""
    
    list_display = ['user', 'blog', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'blog__title', 'review']
    readonly_fields = ['created_at', 'updated_at']


class FavoriteAdmin(admin.ModelAdmin):
    """Admin for Favorite model"""
    
    list_display = ['user', 'blog', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'blog__title']
    readonly_fields = ['created_at']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Favorite, FavoriteAdmin)
