import mistune
from mistune_contrib import math

class JuloParser(mistune.Markdown):
    def __init__(self):
        treeRenderer = JuloDocRenderer()
        blockLexer = mistune.BlockLexer(mistune.BlockGrammar()) #JuloDocBlockLexer()
        inlineLexer = JuloDocInlineLexer(treeRenderer)
        
        super(JuloParser, self).__init__(renderer=treeRenderer, inline=inlineLexer, block=blockLexer)
        
    def output_block_math(self):
        body = self.renderer.placeholder()
        while self.pop()['type'] != 'block_math_end':
            body += self.tok()
        return self.renderer.block_math(body)
"""
class JuloDocBlockLexer(mistune.BlockLexer, math.MathBlockMixin):
    def __init__(self, *args, **kwargs):
        super(JuloDocBlockLexer, self).__init__(*args, **kwargs)
        self.enable_math()
"""

class JuloDocInlineLexer(mistune.InlineLexer, math.MathInlineMixin):
    def __init__(self, renderer, *args, **kwargs):
        super(JuloDocInlineLexer, self).__init__(renderer, *args, **kwargs)
        self.enable_math()

"""
class DocTree(object):
    def __init__(self):
        self.root = ParentNode()
    
    def __iadd__(self, other):
        self.root.children.append(other)
"""

#class DocTreeRenderer(math.MathRendererMixin):
#class DocTreeRenderer(mistune_contrib.Renderer):
class JuloDocRenderer(object):
    def __init__(self, **kwargs):
        self.options = kwargs

    def placeholder(self):
        return ParentNode()
    
    def block_code(self, code, lang=None):
        """Rendering block level code. ``pre > code``.

        :param code: text content of the code block.
        :param lang: language of the given code.
        """
        return BlockCode(code, lang)
    
    def block_quote(self, text):
        return BlockQuote(text)

    def block_html(self, html):
        return BlockHtml(html)
    
    def header(self, text, level, raw=None):
        return Header(text, level, raw)
    
    def hrule(self):
        return HRule()
    
    def list(self, body, ordered=True):
        return List(body, ordered)
    
    def list_item(self, text):
        return ListItem(text)
    
    def paragraph(self, text):
        """Rendering paragraph tags. Like ``<p>``."""
        return Paragraph(text)
    
    # table funcs
    
    def double_emphasis(self, content):
        return SimpleContainer("strong", content)
    def emphasis(self, content):
        return SimpleContainer("em", content)
    def codespan(self, content):
        return SimpleContainer("code", content)
    def linebreak(self):
        return Fixed('<br />\n')
    def strikethrough(self, content):
        return SimpleContainer("del", content)
    def text(self, content):
        return Text(content)
    def escape(self, content):
        return Escape(content)
    def autolink(self, link, is_email=False):
        return AutoLink(link, is_email)
    def link(self, link, title, text):
        return Link(link, title, text) 
    
    def image(self, src, title, text):
        raise Exception("Not implemented")
    
    def inline_html(self, html):
        return InlineHtml(html)
    
    def newline(self):
        return NewLine()
    
    #footnotes
    
    # Math
    
    def block_math(self, text):
        return BlockMath(text)

    def block_latex(self, name, text):
        return BlockLatex(text)

    def math(self, text):
        return InlineMath(text)

class DocNode(object):
    pass

class Fixed(DocNode):
    def __init__(self, text):
        self.text = text
    def __str__(self):
        return self.text
    def toHtml(self):
        return self.text
    
class SimpleContainer(DocNode):
    def __init__(self, name, content):
        self.name = name
        self.content = content
        print("Creating SimpleContainer '" + name + "'")
        
    def __str__(self):
        return self.name + "(" + self.content.__str__() + ")"
    
    def toHtml(self):
        if(isinstance(self.content, DocNode)):
           contentText = self.content.toHtml()
        elif(isinstance(self.content, str)):
            contentText = self.content # TODO escape html
        else:
            return "[unknown content type for container '%s']" % self.name
        return "<%s>%s</%s>" % (self.name, contentText, self.name) 
    
class InlineMath(DocNode):
    def __init__(self, text):
        self.text = text
    
    def __str__(self):
        return "InlineMath(%s)" % self.text
    
    def toHtml(self):
        return "\\( %s \\)" % self.text
class BlockMath(DocNode):
    def __init__(self, text):
        self.text = text
    
    def __str__(self):
        return "BlockMath(%s)" % self.text
    
    def toHtml(self):
        return "$$ %s $$" % self.text
class BlockLatex(DocNode):
    def __init__(self, name, text):
        self.name = name
        self.text = text
    
    def __str__(self):
        return "BlockLatex(%s)" % self.text
    
    def toHtml(self):
        return r'\begin{%s}%s\end{%s}' % (name, text, name)


    
class Text(DocNode):
    def __init__(self, text):
        self.text = text
    def __str__(self):
        return self.text
    
    def toHtml(self):
        # TODO escape
        return self.text

class Link(DocNode):
    def __init__(self, link, title, text):
        self.link = link
        self.title = title
        self.text = text

class AutoLink(DocNode):
    def __init__(self, link, is_email):
        self.link = link
        self.is_email = is_email
        
class List(DocNode):
    def __init__(self, content, ordered):
        self.content = content
        self.ordered = ordered
    
    def __str__(self):
        if self.ordered:
            return "OrderedList(" + self.content.__str__() + ")"
        else:
            return "List(" + self.content.__str__() + ")"
        
    def toHtml(self):
        if(self.ordered):
            tag = "ol"
        else:
            tag = "ul"
        
        return "<%s>%s</%s>" % (tag, self.content.toHtml(), tag)
        
class ListItem(DocNode):
    def __init__(self, content):
        self.content = content
    
    def __str__(self):
        return "ListItem(" + self.content.__str__() + ")"
    
    def toHtml(self):
        return "<li>%s</li>" % (self.content.toHtml())
            
class Escape(DocNode):
    def __init__(self, text):
        self.text = text
    def __str__(self):
        return "Escape(%s)" % self.text
    
    def toHtml(self):
        return self.text # TODO !!!

class NewLine(DocNode):
    def __init__(self):
        pass

class Paragraph(DocNode):
    def __init__(self, content):
        self.content = content
    
    def __str__(self):
        return "Paragraph(" + self.content.__str__() + ")"
    
    def toHtml(self):
        return "<p>" + self.content.toHtml() + "</p>"

        
class Header(DocNode):
    def __init__(self, content, level, raw):
        self.content = content
        self.level = level
        self.raw = raw
    
    def __str__(self):
        return "Header (" + self.content.__str__() + ")"
    
    def toHtml(self):
        return "<h%s>%s</h%s>" % (self.level, self.content.toHtml(), self.level)

class HRule(DocNode):
    pass

class BlockCode(DocNode):
    def __init__(self, code, lang):
        self.code = code
        self.lang = lang

class BlockHtml(DocNode):
    def __init__(self, html):
        self.html = html

class InlineHtml(DocNode):
    def __init__(self, html):
        self.html = html

class BlockQuote(DocNode):
    def __init__(self, content):
        self.content = content



class ParentNode(DocNode):
    def __init__(self):
        #self.type = 
        self.children = []
    
    def __iadd__(self, other):
        self.children.append(other)
        return self
    
    def toHtml(self):
        ret = ''
        for child in self.children:
            if isinstance(child, DocNode):
                childContent = child.toHtml()
            elif isinstance(child, str):
                childContent = child # escape
            else:
                childContent = "[Unknown node type]"
            
            ret += childContent
        return ret
    
    
    def __str__(self):
        ret = "{"
        first = True
        for child in self.children:
            if not first:
                ret += ", "
            ret += child.__str__()
            first = False
        ret += "}"
        return ret

#class JuloDocRenderer(TreeRenderer, math.MathRendererMixin):
#    def __init__(self, *args, **kwargs):
#        super(JuloDocRenderer, self).__init__(*args, **kwargs)
#        #self.enable_math()
