from django.db import models
from django.urls import reverse

class Author(models.Model):
    author_name = models.CharField(max_length = 200)

    def __str__(self):
        return self.author_name

class Article(models.Model):
    article_key    = models.CharField(max_length = 200)
    article_author = models.ForeignKey(Author, on_delete=models.SET_NULL, null = True, blank = True)
    article_title  = models.CharField(max_length = 200)
    article_type   = models.IntegerField(default = 0)
    article_body   = models.CharField(max_length = 15000, blank=True, default='')
    article_modification_date = models.DateTimeField('date modified')

    def __str__(self):
        return "Article '{}' of type {}".format(self.article_key, self.article_type)
    
    
class Node(models.Model):
    node_content = models.ForeignKey(Article, on_delete=models.SET_NULL, null = True, blank = True)
    node_parent = models.ForeignKey('self', on_delete=models.SET_NULL, null = True, blank = True)
    #node_title = models.CharField(max_length = 200, default = '')
    
    def toHtml(self, draw_first = True):
        if not self.node_content:
            node_title = '(null node)'
        else:
            node_title = self.node_content.article_title
        
        ret = ''
        if draw_first:
            if self.node_content != None:
                key   = self.node_content.article_key
                title = self.node_content.article_title
                ret += '<a href="%s">%s</a>' % (reverse('article', args=[key]), title)
            else:
                ret += '(Empty)'
        
        children = self.getChildren()
        if children.count():
            ret += '<ul>\n'
            
            for child in children:
                ret += '<li>\n'
                ret += child.toHtml()
                ret += '</li>\n'
            
            ret += '</ul>'
        return ret
    
    def getChildren(self):
        ret = Node.objects.filter(node_parent=self.id)
        return ret

class Guide(models.Model):
    guide_key = models.CharField(max_length = 200, default='guide1')
    guide_author = models.ForeignKey(Author, on_delete=models.SET_NULL, null = True, blank = True)
    guide_title = models.CharField(max_length = 200, default = '')
    guide_root = models.ForeignKey(Node, on_delete=models.SET_NULL, null = True, blank = True)
    
    def __str__(self):
        return "Guide '" + self.guide_title + "'"
    
    def toHtml(self):
        #et = self.guide_title + '\n'
        ret = ''
        
        if self.guide_root:
            ret += self.guide_root.toHtml(True)
        else:
            ret += '(no guide_root)'
        
        return ret


# article = Article(article_key='biofisica.cinematica',article_title='Cinemática',article_body='La cinemática bla bla bla.',article_author=author,article_type=1,article_modification_date=timezone.now())
