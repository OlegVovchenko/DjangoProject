from django.shortcuts import render, get_object_or_404, redirect
from django.template import context
from django.urls import reverse
from .models import Category, Post, Tag
from django.db.models import Count, Q, F
from django.core.paginator import Paginator
from django.contrib.messages import constants as messages
from django.contrib import messages

MESSAGE_TAGS = {
    messages.DEBUG: 'primary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}


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
    posts= Post.objects.select_related('category', 'author').prefetch_related('tags').all()
    
    search_query= request.GET.get('search_query','')
    if search_query:
        q_object = Q()
        if request.GET.get('search_content') == '1':
            q_object |= Q(content__icontains=search_query)
        if request.GET.get('search_title') == '1':
            q_object |= Q(title__icontains=search_query)
        if request.GET.get('search_tags') == '1':
            q_object |= Q(tags__name__icontains=search_query)
        if request.GET.get('search_category') == '1':
            q_object |= Q(category__name__icontains=search_query)
        if request.GET.get('search_slug') == '1':
            q_object |= Q(slug__icontains=search_query)
        if q_object:
            posts= posts.filter(q_object).distinct()
    sort_by = request.GET.get('sort_by', 'created_date')
    if sort_by == 'view_count':
        posts = posts.order_by('-views')
    elif sort_by == 'update_date':
        posts= posts.order_by('-updated_at')
    else:
        posts= posts.order_by('-created_at')
        
    
    paginator = Paginator(posts, 3) # Показываем по 3 поста на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    messages.add_message(request, messages.SUCCESS, 'Посты успешно отображены')
    context = {
        'title': 'Блог',
        'posts': page_obj,
        'sort_by': sort_by,
        'search_query': search_query,
    }
    return render(request, 'blog.html', context)

def post_detail(request, post_slug):
    post= get_object_or_404(Post, slug=post_slug)
    post= Post.objects.select_related('category', 'author').prefetch_related('tags').get(slug=post_slug)
    sessions= request.session
    key= f"viewed_posts_{post.id}"
    if key not in sessions:
        Post.objects.filter(id=post.id).update(views=F('views') + 1)
        sessions[key]= True
        post.refresh_from_db()

    context= {
        "title": post.title, 
        "post": post
    }
    return render(request, 'post_detail.html', context)

def catalog_categories(request):
    categories= Category.objects.all()
    paginator = Paginator(categories, 5) # Показываем по 5 категорий на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context= {
        "categories": page_obj, 
        "title": "Категории блога"
    }
    return render(request, "catalog_categories.html", context)

def category_create(request):
    if request.method == "POST":
        name= request.POST.get("name")
        description= request.POST.get("description")

        if name:
            category = Category.objects.create(name=name, description=description or "Без описания")
            messages.success(request, f"Категория '{category.name}' успешно создана")
            return redirect("blog:catalog_categories")
    
    context= {
        "title": "Создание категории",
        "button_text": "Создать категорию",
        "action_url": reverse("blog:category_create"),
        "category": None
    }

    return render(request, "category_create.html", context)

def category_update(request, category_slug):
    category: dict[str, str] = Category.objects.get(slug=category_slug)
    if request.method == "POST":
        name= request.POST.get("name")
        description= request.POST.get("description")

        if name:
            category.name= name
            category.description= description or "Без описания"
            category.save()
            messages.success(request, f"Категория '{category.name}' успешно обновлена")
            return redirect("blog:catalog_categories")
    
    context= {
        "title": "Обновление категории",
        "button_text": "Обновить категорию",
        "action_url": reverse("blog:category_update", kwargs={"category_slug": category_slug}),
        "category": category
    }

    return render(request, "category_create.html", context)

def category_detail(request, category_slug):
    category: dict[str, str] = Category.objects.get(slug=category_slug)
    posts= category.posts.all()
    paginator = Paginator(posts, 2) # Показываем по 2 поста на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        "title": f"Категория: {category.name}",
        "category": category,
        "posts": page_obj,
        "active_menu": "categories"
    }
    return render(request, "category_detail.html", context)


def catalog_tags(request):
    tags = Tag.objects.annotate(posts_count=Count('posts')).order_by('-posts_count')
    paginator = Paginator(tags, 3) # Показываем по 3 тега на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "title": "Теги блога",
        "tags": page_obj,
        "active_menu": "tags"
    }
    return render(request, "catalog_tags.html", context)

def tag_detail(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    posts = tag.posts.all()
    paginator = Paginator(posts, 3) # Показываем по 3 поста на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "title": f"Тег: {tag.name}",
        "tag": tag,
        "posts": page_obj,
        "active_menu": "tags"
    }
    return render(request, "tag_detail.html", context)
