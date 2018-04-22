from django.utils import html
from django.utils.safestring import mark_safe
from django import template
from django.templatetags.static import static

from julopedia.models import Node

register = template.Library()

#total_columns = 20

class HierarchyElement:
    def __init__(self, level, node, chain, sibling_index):
        self.level = level
        self.node = node
        self.chain = chain
        self.sibling_index = sibling_index
        
    def get_title_html(self):
        return html.escape(self.node.title)

class SpacingRow:
    def __init__(self, prev_element, post_element, chain):
        self.min = post_element and post_element.level or 0
        self.max = prev_element and prev_element.level + 1 or 0
        
        self.chain = chain
        
    def to_html(self, total_columns):
        ret = ''
        ret += '<tr class="bar">\n    '
        
        for i in range(self.min):
            ret += '<td class="holder_empty"></td>'
        
        for i in range(self.min, self.max + 1):
            if i == self.max:
                colspan = total_columns - self.max
                if(colspan < 1):
                    raise Exception("Not enough columns")
            else:
                colspan = 1
            
            parent_ids = ''
            for j in range(i + 1):
                if j > 0:
                    parent_ids += '_'
                parent_ids += str(self.chain[j][0])
            sibling_index = self.chain[i][1]
            ret += '<td class="holder holder_%s-%s" colspan="%s"></td>' % (parent_ids, sibling_index, colspan) #, parent_ids + '-' + str(sibling_index))
        
        ret += '\n</tr>\n'
        return ret
        

class ElementRow:
    def __init__(self, element):
        self.element = element
    
    def to_html(self, total_columns):
        ret = ''
        ret += '<tr class="element">\n    '
        for i in range(self.element.level):
            ret += '<td class="indent"></td>'
        
        id_chain = ''
        for (index, (id, count)) in enumerate(self.element.chain):
            if index > 0:
                id_chain += '_'
            id_chain += str(id)
        
        sibling_index = self.element.chain[-2][1] - 1
        
        ret += '<td class="handle_cell handle_cell_%s-%s"><div class="handle"><img src="%s" /></div></td>' % (id_chain, sibling_index, static('julopedia/img/arrow.png'))
        ret += '<td colspan="%s" class="content">%s</td>' % (total_columns - self.element.level - 1, self.element.get_title_html())
        
        ret += '\n</tr>\n'
        return ret

@register.simple_tag
def hierarchy_editor(root):
    if not root:
        return 'No root specified'
    
    (elements, max_level) = get_hierarchy_elements(root, [], 0, [(root, 0)])
    
    total_columns = max_level + 2
    
    rows = get_table_rows(elements, total_columns, root.id)
    
    editorHtml = ''
    editorHtml += '<table>'
    
    editorHtml += '<tr>'
    for i in range(total_columns - 1):
        editorHtml += '<th class="header">%s</th>' % ''
    editorHtml += '<th class="header header_last">%s</th>' % ''
    editorHtml += '</tr>\n'
    
    for row in rows:
        editorHtml += row.to_html(total_columns)
    
    """
    for i in range(0, len(elements) + 1):
        editorHtml += draw_bar(elements, i)
        
        if i < len(elements):
            editorHtml += draw_element(elements[i])
    """
    
    editorHtml += '</table>'
    
    return mark_safe(editorHtml)

def get_element(elements, index):
    if index >= 0 and index < len(elements):
        return elements[index]
    else:
        return None

def get_table_rows(elements, total_columns, root):
    ret = []
    for i in range(0, len(elements) + 1):
        prev_index = i - 1
        post_index = i
        
        prev_element = get_element(elements, prev_index)
        post_element = get_element(elements, post_index)
        
        if prev_element:
            chain = prev_element.chain
        else:
            chain = [(root, 0)]
         
        ret.append(SpacingRow(prev_element, post_element, chain))
        
        if i < len(elements):
            ret.append(ElementRow(elements[i]))
    
    return ret

def get_hierarchy_elements(node, buffer, level, chain):
    children = Node.objects.get_children(node)
    
    max_level = level - 1
    
    for (index, child) in enumerate(children):
        current = chain.pop()
        chain.append((current[0], current[1] + 1))
        
        chain.append((child, 0))
        
        id_chain = []
        for (node, count) in chain:
            id_chain.append((node.id, count))
            
        buffer.append(HierarchyElement(level, child, id_chain, index))
        
        (buffer, max_child_level) = get_hierarchy_elements(child, buffer, level + 1, chain)
        max_level = max(max_level, max_child_level)
        
        chain.pop()
    
    return (buffer, max_level)



