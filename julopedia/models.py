from django.db import models

class Author(models.Model):
    author_name = models.CharField(max_length = 200)

    def __str__(self):
        return self.author_name

class Article(models.Model):
    article_key    = models.CharField(max_length = 200)
    article_author = models.ForeignKey(Author, on_delete=models.SET_NULL, null = True, blank = True)
    article_title  = models.CharField(max_length = 200)
    article_type   = models.IntegerField(default = 0)
    article_body   = models.CharField(max_length = 15000)
    article_modification_date = models.DateTimeField('date modified')

    def __str__(self):
        return "Article '{}' of type {}".format(self.article_key, self.article_type)
    
    
class Node(models.Model):
    node_content = models.ForeignKey(Article, on_delete=models.SET_NULL, null = True, blank = True)
    node_parent = models.ForeignKey('self', on_delete=models.SET_NULL, null = True, blank = True)

class Guide(models.Model):
    guide_title   = models.CharField(max_length = 200)
    guide_root = models.ForeignKey(Node, on_delete=models.SET_NULL, null = True, blank = True)
    
    def __str__(self):
        return "Guide '" + self.guide_title + "'"


# article = Article(article_key='biofisica.cinematica',article_title='Cinemática',article_body='La cinemática bla bla bla.',article_author=author,article_type=1,article_modification_date=timezone.now())
