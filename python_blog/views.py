from unicodedata import category
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse

CATEGORIES = [
        {'slug': 'python', 'name': 'Python'},
        {'slug': 'django', 'name': 'Django'},
        {'slug': 'postgresql', 'name': 'PostgreSQL'},
        {'slug': 'docker', 'name': 'Docker'},
        {'slug': 'linux', 'name': 'Linux'},
    ]

def main(request):
    catalog_categories_url: str = reverse('blog:catalog_categories')
    catalog_tags_url: str = reverse('blog:catalog_tags')
    catalog_posts_url: str = reverse('blog:catalog_posts')
    return HttpResponse(f"""
        <h1>Главная страница</h1>
        <p><a href="{catalog_categories_url}">Каталог категорий</a></p>
        <p><a href="{catalog_tags_url}">Каталог тегов</a></p>
        <p><a href="{catalog_posts_url}">Каталог постов</a></p>
    """)

def catalog_posts(request):
    return HttpResponse('Каталог постов')

def post_detail(request, post_slug):
    return HttpResponse(f'Страница поста {post_slug}')

def catalog_categories(request):
    links: list[Any] = []
    for category in CATEGORIES:
        url: str = reverse('blog:category_detail', args=[category['slug']])
        links.append(f'<p><a href="{url}">{category["name"]}</a></p>')


    # Ссылка в reverse на name пути из python_blog.urls
    return HttpResponse(f"""
        <h1>Каталог категорий</h1>
        {''.join(links)}
        <p><a href="{reverse('blog:catalog_posts')}">К списку постов</a></p>
    """)    

def category_detail(request, category_slug):
    category: dict[str, str] = [cat for cat in CATEGORIES if cat['slug'] == category_slug][0]
    if category:
        name: str = category['name']
    else:
        name: Any = category_slug


    # Ссылка в reverse на name пути из python_blog.urls
    return HttpResponse(f"""
    <h1>Категория: {name}</h1>
    <p><a href="{reverse('blog:catalog_categories')}">Назад к категориям</a></p>
""")

def catalog_tags(request):
    return HttpResponse('Каталог тегов')

def tag_detail(request, tag_slug):
    return HttpResponse(f'Страница тега {tag_slug}')
