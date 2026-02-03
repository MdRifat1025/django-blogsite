from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_home, name='blog-home'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog-detail'),
    path('blog/create/', views.blog_create, name='blog-create'),
    path('blog/<slug:slug>/edit/', views.blog_update, name='blog-update'),
    path('blog/<slug:slug>/delete/', views.blog_delete, name='blog-delete'),
    path('blog/<slug:slug>/rate/', views.rate_blog, name='rate-blog'),
    path('blog/<slug:slug>/favorite/', views.add_to_favorites, name='add-favorite'),
    path('blog/<slug:slug>/unfavorite/', views.remove_from_favorites, name='remove-favorite'),
    path('favorites/', views.my_favorites, name='my-favorites'),
    path('category/<slug:slug>/', views.blogs_by_category, name='blog-category'),
    path('author/<str:username>/', views.author_blogs, name='author-blogs'),
]
