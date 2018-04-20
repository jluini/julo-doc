
import pypandoc

def jsonToHtml(json):
        return pypandoc.convert_text(json, 'html', format='json', extra_args=['--mathjax'])
def markdownToJson(md):
        return pypandoc.convert_text(md, 'json', format='markdown') #, extra_args=['--mathjax'])
class t:
    @staticmethod
    def fromMarkdown(md):
        
        print("From %s" % md)
        
        json = markdownToJson(md)
        html = jsonToHtml(json)
        
        ret = JuloTree(json)
        
        return ret

class JuloTree:
    
    def __init__(self, json):
        self.json = json
    
    def toHtml(self):
        return jsonToHtml(self.json)
