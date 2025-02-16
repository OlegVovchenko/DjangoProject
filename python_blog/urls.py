from django.urls import path
from python_blog.views import catalog_posts, post_detail, catalog_categories, category_detail, catalog_tags, tag_detail, category_create, category_update, tag_create

app_name = 'blog'

# Общий префикс posts/
urlpatterns = [
    # Каталог постов
    path('', catalog_posts, name='catalog_posts'),
    
    # Категории
    # Категории posts/categories/
    # Категории posts/categories/python/
    path('categories/', catalog_categories, name='catalog_categories'),
    path('categories/create/', category_create, name='category_create'),
    path('categories/<slug:category_slug>/', category_detail, name='category_detail'),
    path('categories/<slug:category_slug>/update', category_update, name='category_update'),
    path('categories/<slug:category_slug>/delete', category_detail, name='category_detail'),
    
    # Теги
    # Теги posts/tags/
    # Теги posts/tags/python
    path('tags/', catalog_tags, name='catalog_tags'),
    path('tags/create/', tag_create, name='tag_create'),
    path('tags/<slug:tag_slug>/', tag_detail, name='tag_detail'),

    # Посты
    # Посты posts/tags/
    path('<slug:post_slug>/', post_detail, name='post_detail'),
]
