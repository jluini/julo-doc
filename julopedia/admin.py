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
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        print("La vida loca!!!")
        return super().render_change_form(request, context, add=add, change=change, form_url=form_url, obj=obj)
    

admin.site.register(Author)
admin.site.register(Node, NodeAdmin)
