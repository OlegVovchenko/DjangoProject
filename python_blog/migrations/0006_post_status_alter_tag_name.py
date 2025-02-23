# Generated by Django 5.1.4 on 2025-02-23 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('python_blog', '0005_tag_post_slug_alter_post_category_remove_post_tags_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('draft', 'Черновик'), ('review', 'На проверке'), ('review_done', 'Проверено'), ('published', 'Опубликовано')], default='review', max_length=20, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
    ]
