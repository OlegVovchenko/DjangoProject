from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Категория - внешний ключ
    category = models.ForeignKey(
        "Category", # Ссылка на модель категории
        on_delete=models.SET_NULL, # При удалении категории, установить значение NULL
        blank=True, # Не требуем в формах заполнения
        null=True, # Разрешаем значение NULL в базе данных
        related_name="posts", # Имя обратной связи
        default=None # Значение по умолчанию NULL
    )

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True, default='Без описания')


# PRACTICE - Работа с моделью Post
"""
1. Создать новый пост
post = Post(title="Django для чайников", content="Django очень легкий фреймворк, и у него пологая кривая входа...") 
post.save()

INSERT INTO "python_blog_post" ("title", "content", "created_at", "updated_at", "category")
VALUES ('Django для чайников', 'Django очень легкий фреймворк, и у него пологая кривая входа...', '2024-12-23 17:31:02.040654', '2024-12-23 17:31:02.040654', NULL) RETURNING "python_blog_post"."id"
Execution time: 0.000996s [Database: default]


post_1 = post

post_2 = Post(title="Базы данных для продавцов котиков", content="Теперь вы сможете каждого котика сохранить в базе данных")

Django ORM ленива.
Все запросы по умолчанию выполняются в ленивом режиме.
Допустим при сохранении, запрос будет выполнен только при вызове метода save()

При чтении, запрос выполнен при обращении к результату запроса

2. Получить все посты

posts = Post.objects.all()
posts = <QuerySet [<Post: Post object (1)>, <Post: Post object (2)>]>

Что такое QuerySet?
QuerySet - это набор объектов, которые мы получили из базы данных.
Мы можем использовать QuerySet для фильтрации, сортировки, группировки и других операций над объектами.

post_1 = post[0]
post_1

post_1.title
post_1.content
post_1.created_at

post_1.content = "Django не очень легкий фреймворк, но у него кривая входа..."
post_1.save()

post_3 = Post(title="Тестовый пост", content="Тестовый пост")

#  Делаем операцию удаления
post_3.delete()

3. Получить пост по id
post_1 = Post.objects.get(id=1) # id - поле модели id - это поле, которое автоматически генерируется Django
post_1 = Post.objects.get(pk=1) # pk - primary key - первичный ключ

4. Получим все посты и сортируем их по полю created_at от новых к старым
posts = Post.objects.all().order_by("-created_at")

5. Используя filter получим посты, где категория NULL
posts = Post.objects.filter(category=None)
Применим к полученному QuerySet сортировку
posts = posts.order_by("-created_at")

6.
"""