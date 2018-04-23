from django.utils import html
from django.utils.safestring import mark_safe
from django import template
from django.templatetags.static import static

from julopedia.models import Node
from _sqlite3 import Row

register = template.Library()

#total_columns = 20

class HierarchyElement:
    def __init__(self, chain):
        self.chain = chain
        
    def get_title_html(self):
        h = self.head()
        if h:
            return html.escape(h.title)
        else:
            return '(root)'
    def level(self):
        return len(self.chain) - 1
    def head(self):
        #print('%s --> %s' % (self.chain, self.chain[-1][0]))
        return self.chain[-1][0]
    
    def __str__(self):
        return str(self.chain) + ': ' + self.get_title_html()
    
class SpacingRow:
    def __init__(self, chain, min_level, total_columns):
        self.chain = chain
        self.min_level = min_level
        self.total_columns = total_columns
    
    def is_spacing_row(self):
        return True
    
    def to_html(self):
        ret = ''
        #print(self.min_level, self.chain)
        for i in range(self.min_level):
            ret += '<td class="holder_empty"></td>'
        for i in range(self.min_level, len(self.chain)):
            chain_str = ''
            for j in range(i + 1):
                (node, count) = self.chain[j]
                chain_str += '_%s' % (node and node.id or 'N')
            
            sibling_index = self.chain[i][1]
            
            chain_str += '-%s' % (sibling_index)
                
            ret += '<td class="holder holder%s">+</td>' % chain_str
        
        if self.total_columns > len(self.chain):
            ret += '<td colspan="%s"></td>' % (self.total_columns - len(self.chain))
        
        return mark_safe(ret)
    
class ElementRow:
    def __init__(self, element, total_columns):
        self.element = element
        self.total_columns = total_columns
        
    def is_spacing_row(self):
        return False
    
    def __str__(self):
        return self.element.__str__()
    
    def to_html(self):
        ret = ''
        level = len(self.element.chain) - 1
        
        for i in range(level - 1):
            ret += '<td class="indent"></td>'
        
        colspan = self.total_columns - (level - 1)
        
        chain_str = ''
        for (node, count) in self.element.chain:
            chain_str += '_%s' % (node and node.id or 'N')
        
        chain_str += '-%s' % (self.element.chain[-2][1] - 1)
        
        ret += '<td class="handle_cell handle_cell%s" colspan="%s"><div class="handle"><img src="%s" /> %s</div></td>' % (chain_str, colspan, static('julopedia/img/arrow.png'), self.element.get_title_html())
        
        return mark_safe(ret)

@register.inclusion_tag('admin/julopedia/node/hierarchy_tree.html')
def hierarchy_tree(root):
    (elements, max_level) = get_hierarchy_elements([], [(root, 0)])
    
    print('\n')
    for e in elements:
        print(e)
    print('\n')
    
    total_columns = max_level + 2
    rows = get_table_rows(elements, total_columns)
    
    #print('\n')
    #for r in rows:
    #    print(r)
    #print('\n')
    
    columns = ['header'] * (total_columns - 1)
    columns.append('header header_last')
    
    return {
        'columns': columns,
        'table_rows': rows,
    }

def get_table_rows(elements, total_columns):
    ret = []
    for index in range(len(elements)):
        element = elements[index]
        
        if index > 0:
            ret.append(ElementRow(element, total_columns))
        
        if index == len(elements) - 1:
            next_level = 0
        else:
            next_level = elements[index + 1].level() - 1
        ret.append(SpacingRow(element.chain, next_level, total_columns))
        
    
    return ret

def get_hierarchy_elements(elements, parent_chain): #, root, sibling_index):
    max_level = len(parent_chain) - 1
    
    element = HierarchyElement(list(parent_chain))
    elements.append(element)
    
    root = parent_chain[-1][0]
    
    for child in Node.objects.get_children(root):
        (root, count) = parent_chain.pop()
        parent_chain.append((root, count + 1))
        parent_chain.append((child, 0))
        (elements, child_max_level) = get_hierarchy_elements(elements, parent_chain)
        parent_chain.pop()
        max_level = max(max_level, child_max_level)
        
    return (elements, max_level)
    