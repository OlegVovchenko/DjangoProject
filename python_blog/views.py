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

MENU_ITEMS = [
        {"title": "Главная", "url_name": "main"},
        {"title": "Все посты", "url_name": "blog:catalog_posts"},
        {"title": "Категории", "url_name": "blog:catalog_categories"},
        {"title": "Теги", "url_name": "blog:catalog_tags"},
]

def main(request):
    catalog_categories_url: str = reverse('blog:catalog_categories')
    catalog_tags_url: str = reverse('blog:catalog_tags')

    context = {
        "title": "Главная страница",
        "text": "Текст главной страницы",
        "user_status": "admin",
        "menu_items": MENU_ITEMS,

    }
    return render(request, "main.html", context)


def catalog_posts(request):
    return HttpResponse('Каталог постов')

def post_detail(request, post_slug):
    return HttpResponse(f'Страница поста {post_slug}')

def catalog_categories(request):
    links: list[Any] = []
    for category in CATEGORIES:
        url: str = reverse('blog:category_detail', args=[category['slug']])
        links.append(f'<p><a href="{url}">{category["name"]}</a></p>')


    context: dict[str, Any] = {
        "title": "Категории",
        "text": "Текст страницы с категориями",
        "categories": CATEGORIES,
    }
    return render(request, "catalog_categories.html", context)

def category_detail(request, category_slug):
    category: dict[str, str] = [cat for cat in CATEGORIES if cat['slug'] == category_slug][0]
    if category:
        name: str = category['name']
    else:
        name: Any = category_slug

    context: dict[str, str] = {
        "title": f"Категория {name}",
        "text": f"Текст категории {name}",
    }

    return render(request, "category_detail.html", context)

def catalog_tags(request):
    return HttpResponse('Каталог тегов')

def tag_detail(request, tag_slug):
    return HttpResponse(f'Страница тега {tag_slug}')
