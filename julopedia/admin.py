from django.contrib import admin
from django import forms

# Register your models here.

from .models import Author, Node


class NodeModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        fields = '__all__'
        model = Node
    

class NodeAdmin(admin.ModelAdmin):
    form = NodeModelForm

admin.site.register(Author)
admin.site.register(Node, NodeAdmin)
