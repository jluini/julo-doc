
from julodoc.tree.julotree import t, JuloTree

from julopedia.models import Author, Node
from django.utils import timezone

import pypandoc
from pandocfilters import applyJSONFilters, Str

import json

def xper():
    authors = Author.objects.all()
    if not len(authors):
        print("No hay autores")
        return
    author = authors[0]
    node = Node(
        node_type = 1,
        title = "Título",
        content = "# Heading\n\nEste es un párrafo.\n\n# Otro heading\n\nOtro párrafo.\n",
        author = author,
        modification_date = timezone,
        parent = None
    )
    
    print("Node created")
    print(node)
    print("   OK")
    
    tree = t.fromMarkdown(node.content)
    
    print(tree.json)
    
    print("------------------")
    
    print(tree.toHtml())
    
    def toCaps(key, value, format, meta):
        if key == 'Str':
            return Str(value.upper())
    
    jsonText = applyJSONFilters([toCaps], tree.json, "")
    
    class Obj:
        def __init__(self, str):
            self.str = str
        def read(self):
            return self.str
    
    obj = Obj(jsonText)
    
    jsonTree = json.load(obj)
    
    return jsonTree
    

def nodeToHtml(node):
    markdown = node.content
    #ret = pypandoc.convert_text(article.article_body, 'html', format='markdown+tex_math_double_backslash', extra_args=['--mathjax'])
    ret = pypandoc.convert_text(markdown, 'html', format='markdown', extra_args=['--mathjax'])
    
    return ret