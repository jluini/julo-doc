from django.db import models
from django.urls import reverse
from django.template.defaultfilters import title
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from julodoc.tree import julotree

class NodeManager(models.Manager):
    def get_children(self, node):
        return self.filter(parent=node.id)
    
    def get_by_path(self, path):
        if not isinstance(path, (list, tuple)):
            raise Node.DoesNotExist("Node with path " + path.join("//"))
        elif len(path) == 0:
            raise Node.DoesNotExist("Empty path")
        
        node = None
        for token in path:
            try:
                if(node == None):
                    node = self.get(parent=None,    node_key=token)
                else:
                    node = self.get(parent=node.id, node_key=token)
                
            except ObjectDoesNotExist:
                raise Node.DoesNotExist("child with key '%s'" % token)
            
        if not node:
            raise Exception("Node expected")
        
        return node
    
class Author(models.Model):
    author_name = models.CharField(max_length = 200)

    def __str__(self):
        return self.author_name
    
    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')

valid_key = RegexValidator(julotree.key_regex)

class Node(models.Model):
    # Manager
    objects = NodeManager()
    
    # Fields
    node_type = models.IntegerField(default = 0, verbose_name=_('type'), choices = (
        (0, _("section")),
        (1, _("theory")),
        (2, _("exercise")),
    ))
    
    node_key = models.CharField(max_length = 200, verbose_name=_('key'), validators=[valid_key])
    title  = models.CharField(max_length = 200, verbose_name=_('title'))
    content = models.CharField(max_length = 15000, blank=True, default='', verbose_name=_('content'))
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null = True, blank = True, verbose_name=_('author'))
    
    numbering = models.BooleanField(default=True,verbose_name=_('numbering'))
    
    created_time = models.DateTimeField(editable=False)
    modified_time = models.DateTimeField(editable=False)
    
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null = True, blank = True) #, editable=False)
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_time = timezone.now()
        self.modified_time = timezone.now()
        
        return super(Node, self).save(*args, **kwargs)
    
    class Meta:
        order_with_respect_to = 'parent'
        verbose_name = _('node')
        verbose_name_plural = _('nodes')
    
    def __str__(self):
        return self.title
