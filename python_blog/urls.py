from django.urls import path

urlpatterns = [
    path('/', main, name='main'),
    path('/posts/', catalog_posts, name='catalog_posts'),
    path('/posts/categories/', catalog_categories, name='catalog_categories'),
    path('/posts/categories/<slug:category_slug>/', category_detail, name='category_detail'),
    path('/posts/tags/', catalog_tags, name='catalog_tags'),
    path('/posts/tags/<slug:tag_slug>/', tag_detail, name='tag_detail'),
    path('/posts/<slug:post_slug>/', post_detail, name='post_detail'),
]
