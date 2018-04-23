from django import forms
from django.contrib import admin
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _

# Register your models here.

from .models import Author, Node

class NodeModelForm(forms.ModelForm):
    def capitalize_text(text):
        return text.capitalize()
    capitalize_lazy = lazy(capitalize_text, str)
    content = forms.CharField(widget=forms.Textarea, required=False, label=capitalize_lazy(_('content')))
    
    class Meta:
        fields = '__all__'
        model = Node
    

class NodeAdmin(admin.ModelAdmin):
    form = NodeModelForm
    list_display = ('title', 'node_key', 'author', 'node_type')
    
admin.site.register(Author)
admin.site.register(Node, NodeAdmin)
