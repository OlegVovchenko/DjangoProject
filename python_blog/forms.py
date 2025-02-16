from django import forms
from .models import Tag, Post, Category

class TagForm(forms.Form):
    name = forms.CharField(max_length=200, min_length=2, label="Название", help_text="Введите название тега",required=True)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if Tag.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Тег с таким названием уже существует")
        return name
    class Meta:
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'name': {
                'required': "Название тега обязательно для заполнения",
                'min_length': "Минимальная длина названия тега 2 символа",
                'max_length': "Максимальная длина названия тега 200 символов",
            }
        }