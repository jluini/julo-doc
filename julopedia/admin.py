from django.contrib import admin
from django import forms

# Register your models here.

from .models import Author, Article, Guide, Node


class ArticleModelForm(forms.ModelForm):
    article_body = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        fields = '__all__'
        model = Article
    

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleModelForm

admin.site.register(Article, ArticleAdmin)


admin.site.register(Author)

admin.site.register(Guide)
admin.site.register(Node)


