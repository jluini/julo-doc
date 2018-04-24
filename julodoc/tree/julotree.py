
import re
import pypandoc

def jsonToHtml(json, level):
        return pypandoc.convert_text(json, 'html', format='json', extra_args=['--mathjax','--base-header-level=' + str(level)])


def markdownToJson(md):
        return pypandoc.convert_text(md, 'json', format='markdown-raw_html')

key_regex = re.compile('^[A-Za-z][A-Za-z0-9\-\.\_]*$')

class t:
    @staticmethod
    def fromMarkdown(md):
        json = markdownToJson(md)
        
        ret = JuloTree(json)
        return ret

class JuloTree:
    def __init__(self, json):
        self.json = json
    
    def toHtml(self, level=1):
        return jsonToHtml(self.json, level)
