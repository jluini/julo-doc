from .models import Article

from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import Http404

#import mistune_contrib
#from mistune_.contrib import math

import re # regular expressions
from .julodoc.doctree import JuloParser, ParentNode 

# Create your views here.

def index(request):
    return render(request, 'julopedia/index.html')



def article(request, article_path):
    article_key = getKeyFromPath(article_path)
    
    #return HttpResponse("holitas")

    try:
        article = Article.objects.get(article_key=article_key)
        
        #treeRenderer = DocTreeRenderer()
        #parser = mistune.Markdown(renderer=treeRenderer, inline=None, block=None)
        
        parser = JuloParser()
        
        tree = parser.parse(article.article_body)
        
        print(tree)
        
        #text = traverse(tree, 0)
        
        #text = tree.toHtml()
        text = tree.__str__()
        
        
         
        return render(
            request,
            'julopedia/article.html',
            {
                'article': article,
                'text':    text
            }
        )
        
    except Article.DoesNotExist:
        raise Http404('Article does not exist')
        
    #return HttpResponse("You're looking at article '%s'." % article_key)


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
    pattern = re.compile('^[A-Za-z][A-Za-z0-9\-]*$')
    
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