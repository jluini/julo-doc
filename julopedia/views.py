from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import Http404
#from django.urls import reverse

from django.utils import timezone

from .models import Article, Guide, Node, Author


import re # regular expressions

import pypandoc

# Create your views here.

def index(request):
    guides = Guide.objects.order_by('guide_title')
    articles = Article.objects.order_by('article_title')
    
    return render(
        request,
        'julopedia/index.html',
        {
            'articles': articles,
            'guides': guides,
        }
    )

def article(request, article_path):
    article_key = getKeyFromPath(article_path)
    
    try:
        article = Article.objects.get(article_key=article_key)
        
        articleHtml = articleToHtml(article) 
         
        return render(
            request,
            'julopedia/article.html',
            {
                'article': article,
                'articleHtml': articleHtml
            }
        )
        
    except Article.DoesNotExist:
        raise Http404('Article does not exist')
        
    #return HttpResponse("You're looking at article '%s'." % article_key)

def guide(request, guide_path):
    guide_key = getKeyFromPath(guide_path)
    
    try:
        guide = Guide.objects.get(guide_key=guide_key)
        guideHtml = guide.toHtml()
        
        return render(
            request,
            'julopedia/guide.html',
            {
                'guide': guide,
                'guideHtml': guideHtml,
            }
        )
    except Guide.DoesNotExist:
        raise Http404('Guide does not exist')
        

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
    
    guides = Guide.objects.all()
    
    if guides.count():
        guide = guides[0]
        ret += '<li>Already a guide</li>'
    elif Node.objects.all().count() > 0:
        ret += '<li>Nodes but no guide</li>'
    else:
        createGuide(author)
        ret += '<li>Guide created</li>'
    
    return HttpResponse(ret)
    
def createGuide(author):
    now = timezone.now()
    
    root = newNode(author, 'biofisica',                  'Introducción',          'La **biofísica** bla bla *bla*.', None)
    meca = newNode(author, 'biofisica.mecanica',         'Unidad 1: Mecánica',    'La **mecánica** bla bla *bla*.', root)
    newNode       (author, 'biofisica.cinematica',       'Cinemática',            'La **cinemática** bla bla *bla*.', meca)
    newNode       (author, 'biofisica.dinamica',         'Dinámica',              'La **dinámica** bla bla *bla*.', meca)
    flui = newNode(author, 'biofisica.fluidos',          'Unidad 2: Fluidos',     'Los **fluidos** bla bla *bla*.', root)
    newNode       (author, 'biofisica.fluidos_intro',    'Introducción',          'Los **fluidos** bla bla *bla*.', flui)
    newNode       (author, 'biofisica.prensa',           'Principio de Pascal y prensa hidráulica',          'Bla *bla* **bla**.', flui)
    
    guide = Guide(
        guide_key = 'biofisica',
        guide_author = author,
        guide_title = "Biofísica CBC",
        guide_root = root
    )
    guide.save()
    
    return guide
    
def newNode(author, keyy, title, content, parentNode):
    article = Article(
        article_key = keyy,
        article_author = author,
        article_title = title,
        article_type = 0,
        article_body = content,
        article_modification_date = timezone.now()
    )
    article.save()
    node = Node(node_content = article, node_parent = parentNode)
    node.save()
    
    return node
    
    """
    mecanica = Article(
        article_key = 'biofisica.mecanica',
        article_author = author,
        article_title = 'Unidad 1: Mecánica',
        article_type = 0,
        article_body = 'La **mecánica** bla bla *bla*.',
        article_modification_date = now
    )
    mecanica.save()
    mecanica_node = Node(node_content = mecanica, node_parent = root)
    mecanica_node.save()
    
    cinematica = Article(
        article_key = 'biofisica.cinematica',
        article_author = author,
        article_title = 'Cinemática',
        article_type = 0,
        article_body = 'La **cinemática** bla bla *bla*.',
        article_modification_date = now
    )
    cinematica_node = Node(node_content = cinematica, node_parent = mecanica_node)
    
    dinamica = Article(
        article_key = 'biofisica.dinamica',
        article_author = author,
        article_title = 'Dinámica',
        article_type = 0,
        article_body = 'La **dinámica** bla bla *bla*.',
        article_modification_date = now
    )
    dinamica_node = Node(node_content = dinamica, node_parent = mecanica_node)
    
    fluidos = Article(
        article_key = 'biofisica.fluidos',
        article_author = author,
        article_title = 'Unidad 2: Fluidos',
        article_type = 0,
        article_body = 'Los **fluidos** bla bla *bla*.',
        article_modification_date = now
    )
    fluidos_node = Node(node_content = fluidos, node_parent = root)
    
    fluidos_intro = Article(
        article_key = 'biofisica.fluidos_intro',
        article_author = author,
        article_title = 'Introducción',
        article_type = 0,
        article_body = 'Los **fluidos** bla bla *bla*.',
        article_modification_date = now
    )
    fluidos_intro_node = Node(node_content = fluidos_intro, node_parent = fluidos_node)
    
    pascal_prensa = Article(
        article_key = 'biofisica.pascal_prensa',
        article_author = author,
        article_title = 'Principio de Pascal y prensa hidráulica',
        article_type = 0,
        article_body = 'Bla bla *bla*.',
        article_modification_date = now
    )
    pascal_prensa_node = Node(node_content = pascal_prensa, node_parent = fluidos_node)
    
    """


def articleToHtml(article):
    #ret = pypandoc.convert_text(article.article_body, 'html', format='markdown+tex_math_double_backslash', extra_args=['--mathjax'])
    ret = pypandoc.convert_text(article.article_body, 'html', format='markdown', extra_args=['--mathjax'])
    return ret

def guideToHtml(guide):
    return guide.guide_root.toHtml()

"""
def nodeToHtml(node, root = True):
    if not node.node_content:
        node_title = '(null node)'
    else:
        node_title = node.node_content.article_title
    
    ret = ''
    if True: #not root:
        #ret = node_title + '\n'
        if node.node_content != None:
            key   = node.node_content.article_key
            title = node.node_content.article_title
            ret += '<a href="%s">%s</a>' % (reverse('article', args=[key]), title)
        else:
            ret += 'Empty'
    
    ret += '<ul>\n'
    
    for child in getChildren(node):
        ret += '<li>\n'
        ret += nodeToHtml(child, False)
        ret += '</li>\n'
    
    ret += '</ul>'
    return ret
"""

def traverse(tree, level, buf = ''):
    if isinstance(tree, ParentNode):
        level = level + 1
        for child in tree.children:
            buf = traverse(child, level + 1, buf)
    else:
        for i in range(level):
            buf += "    "
        buf += tree.__str__()
        buf += '\n'
    
    return buf
    
def getKeyFromPath(path):
    pattern = re.compile('^[A-Za-z][A-Za-z0-9\-\.]*$')
    
    ret = ''
    first = True
    for p in path.split('/'):
        if not pattern.match(p):
            raise Http404('Invalid article key')
        
        if not first:
            ret += '.'
        ret += p
        first = False
    
    return ret