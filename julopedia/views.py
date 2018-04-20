from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import Http404
from django.utils import timezone
from django.utils.translation import gettext as _
from django.urls import reverse

import re # regular expressions

from .models import Node, Author
from julodoc.tree.julotree import t, JuloTree

# Create your views here.

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

def node(request, node_path_str):
    node_path = getPathFromString(node_path_str)
    try:
        node = Node.objects.get_by_path(node_path)
        body_html = nodeToHtml(node) 
        
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
        
    #return HttpResponse("You're looking at article '%s'." % article_key)

def get_toc(node, current_path = '', current_section = ''):
    children = Node.objects.get_children(node)
    if not children:
        return ''
    
    if current_path == '':
        current_path = node.node_key
    
    ret = '<ul>'
    i = 0
    for index, child in enumerate(children):
        section = current_section
        if section != '':
            section += '.'
        section += str(index + 1)
        
        child_path = current_path + '/' + child.node_key
        
        ret += '<li>'
        ret += section + ' '
        ret += '<a href="%s">%s</a>' % (reverse('node', args=[child_path]), child.title)
        ret += '</li>'
        ret += get_toc(child, child_path, section)
        
        i += 1
    
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
    
    root = newNode(0, 'biofisica',                  'Introducción',          'La **biofísica** bla bla *bla*.', author, None)
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


def nodeToHtml(node):
    markdown = node.content
    
    ret = t.fromMarkdown(markdown).toHtml()
    
    return ret

def getPathFromString(path_str):
    ret = []
    
    pattern = re.compile('^[A-Za-z][A-Za-z0-9\-\.]*$')
    
    for p in path_str.split('/'):
        if not pattern.match(p):
            raise Http404('Invalid node path')
        ret.append(p)
    
    return ret