from django import forms
from .models import Tag, Post, Category
from django.utils.text import slugify
from unidecode import unidecode

class TagForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        min_length=2,
        label="Название",
        help_text="Введите название тега",
        required=True,
        error_messages={
            'required': "Название тега обязательно для заполнения",
            'min_length': "Минимальная длина названия тега 2 символа",
            'max_length': "Максимальная длина названия тега 200 символов",
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например: Python',
            'id': 'tag-name'
        })
    )
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if Tag.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Тег с таким названием уже существует")
        return name
    
class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['tags_input'].initial = ', '.join(tag.name for tag in instance.tags.all())
    tags_input = forms.CharField(
        label="Теги",
        help_text="Введите теги через запятую",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например: Python, Django, разработка',
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок поста',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст поста',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

    def clean_tags_input(self):
        tags_input = self.cleaned_data.get('tags_input', '')
        if tags_input:
            return [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]
        return []
    
    def clean_title(self):
        title = self.cleaned_data['title']
        # Проверяем существование поста с таким заголовком, исключая текущий пост
        if self.instance.pk:  # Если это обновление существующего поста
            exists = Post.objects.exclude(pk=self.instance.pk).filter(title__iexact=title).exists()
        else:  # Если это создание нового поста
            exists = Post.objects.filter(title__iexact=title).exists()
            
        if exists:
            raise forms.ValidationError("Пост с таким заголовком уже существует")
        return title


    def save(self, commit=True):
        post = super().save(commit=False)
        post.status = 'review'

        if commit:
            post.save()
            tags = self.cleaned_data.get('tags_input', [])
            for tag_name in tags:
                tag_slug = slugify(unidecode(tag_name))
                tag, created = Tag.objects.get_or_create(slug=tag_slug, defaults={"name": tag_name})
                post.tags.add(tag)
                
        return post