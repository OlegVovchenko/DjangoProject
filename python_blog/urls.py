from django.urls import path
from python_blog.views import catalog_posts, post_detail, catalog_categories, category_detail, catalog_tags, tag_detail

urlpatterns = [
    path('', catalog_posts, name='catalog_posts'),
    path('<slug:post_slug>/', post_detail, name='post_detail'),

    # Категории
    path('categories/', catalog_categories, name='catalog_categories'),
    path('categories/<slug:category_slug>/', category_detail, name='category_detail'),
    
    # Теги
    path('tags/', catalog_tags, name='catalog_tags'),
    path('tags/<slug:tag_slug>/', tag_detail, name='tag_detail'),
]
