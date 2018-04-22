from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import Http404
from django.utils import timezone
from django.utils import html
from django.utils.translation import gettext as _, gettext_lazy
from django.urls import reverse
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View

import re # regular expressions

from .models import Node, Author
from julodoc.tree.julotree import t, JuloTree, key_regex

# Create your views here.

class DocumentView(TemplateResponseMixin, ContextMixin, View):
    template_name = 'admin/documents.html'
    extra_context = { 'title': gettext_lazy('Documents') }
    
    def get(self, request, *args, **kwargs):
        context = self.get_context(request)
        return self.render_to_response(context)
    
    def get_context(self, request):
        return {
            'has_permission': request.user.is_active and request.user.is_staff,
            'site_url': '/',
            'root_nodes': Node.objects.filter(parent = None)
        }
        


def index(request):
    root_nodes = Node.objects.filter(parent = None)
    
    return render(
        request,
        'julopedia/index.html',
        {
            'nodes': root_nodes,
            #'guides': guides,
        }
    )

def node(request, node_path_str, ):
    recursive = not request.GET.get('plain')
    
    node_path = getPathFromString(node_path_str)
    try:
        node = Node.objects.get_by_path(node_path)
        body_html = node_to_html(node, recursive, 2) 
        
        toc_html = get_toc(node)
        
        return render(
            request,
            'julopedia/node.html',
            {
                'node': node,
                'tocHtml': toc_html,
                'bodyHtml': body_html,
            }
        )
        
    except Node.DoesNotExist:
        raise Http404("Node with path '%s' does not exist" % '//'.join(node_path))
        
def get_toc(node, current_path = '', current_section = ''):
    children = Node.objects.get_children(node)
    if not children:
        return ''
    
    if current_path == '':
        current_path = html.escape(node.node_key)
    
    ret = '<ul>'
    i = 0
    for child in children:
        if child.numbering:
            section = current_section
            if section != '':
                section += '.'
            section += str(i + 1)
            i += 1
        else:
            section = ''
        
        child_path = current_path + '/' + html.escape(child.node_key)
        
        ret += '<li>'
        ret += section + ' '
        
        
        ret += '<a href="%s">%s</a>' % (reverse('node', args=[child_path]), html.escape(child.title))
        ret += '</li>'
        ret += get_toc(child, child_path, section)
    
    ret += '</ul>'
    return ret

def createData(request, author_name):
    ret = '<li>Creating data</li>'
    
    authors = Author.objects.all()
    
    if authors.count():
        author = authors[0]
        ret += '<li>Already created author</li>' 
    else:
        author = Author(author_name='Julián Luini')
        ret += '<li>Author created</li>'
        author.save()
    
    nodes = Node.objects.all()
    
    if nodes.count():
        node = nodes[0]
        ret += '<li>Already a node</li>'
    else:
        createGuide(author)
        ret += '<li>Guide created</li>'
    
    return HttpResponse(ret)
    
def createGuide(author):
    now = timezone.now()
    
    root = newNode(0, 'biofisica',        'Biofísica',             'La **biofísica** bla bla *bla*.', author, None)
    meca = newNode(0, 'mecanica',         'Unidad 1: Mecánica',    'La **mecánica** bla bla *bla*.', author, root)
    newNode       (1, 'cinematica',       'Cinemática',            'La **cinemática** bla bla *bla*.', author, meca)
    newNode       (1, 'dinamica',         'Dinámica',              'La **dinámica** bla bla *bla*.', author, meca)
    flui = newNode(0, 'fluidos',          'Unidad 2: Fluidos',     'Los **fluidos** bla bla *bla*.', author, root)
    newNode       (1, 'fluidos_intro',    'Introducción',          'Los **fluidos** bla bla *bla*.', author, flui)
    newNode       (1, 'prensa',           'Principio de Pascal y prensa hidráulica',          'Bla *bla* **bla**.', author, flui)
    
    """
    guide = Guide(
        guide_key = 'biofisica',
        guide_author = author,
        guide_title = "Biofísica CBC",
        guide_root = root
    )
    guide.save()
    """
    
    return root
    
def newNode(node_type, keyy, title, content, author, parentNode):
    node = Node(
        node_type = node_type,
        node_key = keyy,
        title = title,
        content = content,
        author = author,
        parent = parentNode,
    )
    node.save()
    
    return node


def node_to_html(node, recursive = True, level=2):
    markdown = node.content
    
    ret = t.fromMarkdown(markdown).toHtml(level = level)
    
    if recursive:
        children = Node.objects.get_children(node)
        
        for child in children:
            ret += '<h%s>%s</h%s>' % (level, html.escape(child.title), level)
            ret += node_to_html(child, True, level + 1)
        
    return ret

def getPathFromString(path_str):
    ret = []
    
    #pattern = 
    
    for node_key in path_str.split('/'):
        if not key_regex.match(node_key):
            raise Http404('Invalid node key "%s"' % node_key)
        ret.append(node_key)
    
    return ret
