import re
from sre_parse import CATEGORIES
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from .blog_data import dataset
from .models import Category, Post


def main(request):
    catalog_categories_url: str = reverse('blog:catalog_categories')
    catalog_tags_url: str = reverse('blog:catalog_tags')

    context = {
        "title": "Главная страница",
        "text": "Текст главной страницы",
        "user_status": "admin",
    }
    return render(request, "main.html", context)

def about(request):

    context = {
        "title": "О компании",
        "text": "Мы - команда профессионалов в области веб-разработки",
    }
    return render(request, "about.html", context)


def catalog_posts(request):
    # Получаем все опубликованные посты
    posts = [post for post in dataset if post['is_published']]
    context = {
        'title': 'Блог',
        'posts': posts
    }
    return render(request, 'blog.html', context)

def post_detail(request, post_slug):
    post = next((post for post in dataset if post['slug'] == post_slug), None)
    
    context = {
        'title': post['title'],
        'post': post
    }
    return render(request, 'post_detail.html', context)

def catalog_categories(request):
    
    CATEGORIES = Category.objects.all()

    context: dict[str, Any] = {
        "title": "Категории",
        "text": "Текст страницы с категориями",
        "categories": CATEGORIES,
    }
    return render(request, "catalog_categories.html", context)

def category_detail(request, category_slug):
    category: dict[str, str] = Category.objects.filter(slug=category_slug).first()
    posts: list[dict[str, str]] = Post.objects.filter(category=category)

    return render(request, "category_detail.html", {"category": category, "posts": posts})


def catalog_tags(request):
    return HttpResponse('Каталог тегов')

def tag_detail(request, tag_slug):
    return HttpResponse(f'Страница тега {tag_slug}')
