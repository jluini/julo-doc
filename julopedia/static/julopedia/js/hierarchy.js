
//var Hierarchy;

(function() {
    
    $(document).ready(function() {
        var hh = new HH();
    });
    
    function HH() {
        
        $('.handle').draggable({
            revert: 'invalid',
            cursorAt: { top: 14, left: 14 },
            helper: 'clone' /*function( event ) {
                var draggableName = $(this).parent().next().html();
                return $("<div class='ui-widget-header'>" + draggableName + "</div>" );
            }*/
        });
        
        $('.holder').droppable({
            //accept: '.handle',
            accept: function(draggable) {
                var draggableData = getHandleData(draggable);
                
                var holderData = getHolderData($(this));
                
                //console.log('Trying to move ' + draggableData.id_chain + '(' + draggableData.sibling_index + ')' + ' to ' + holderData.id_chain + ' as ' + holderData.sibling_index);
                
                var draggableId = draggableData.id_chain[draggableData.id_chain.length - 1];
                var draggableIndex = draggableData.sibling_index;
                var parentId = draggableData.id_chain[draggableData.id_chain.length - 2];
                var holderId    = holderData.id_chain[holderData.id_chain.length - 1];
                var holderIndex = holderData.sibling_index;
                
                //console.log(parentId, holderId, draggableIndex, holderIndex);
                if(holderData.id_chain.includes(draggableId)) {
                    return false;
                } else if(holderId == parentId && (draggableIndex == holderIndex || draggableIndex == holderIndex - 1)) {
                    return false;
                }
                return true;
            },
            
            classes: {
                'ui-droppable-hover': 'holder_hover',
                'ui-droppable-active': 'holder_active'
            }
        });
        
    }
    
    function getHolderData(holder) {
        var cssClasses = holder.attr('class').split(' ');
        
        for(var i = 0; i < cssClasses.length; i++) {
        var cssClass = cssClasses[i]
            m = cssClass.match('holder_([0-9\_]*)-([0-9]*)')
            
            if(m) {
                chain_str = m[1]
                index = parseInt(m[2], 10);
                
                return {
                    id_chain: chain_str.split('_').map(function(idstr) { return parseInt(idstr, 10); }),
                    sibling_index: index
                }
            }
        }
        console.log('not found');
        return false;
    }
    
    function getHandleData(handle) {
        var cssClasses = handle.parent().attr('class').split(' ');
        for(var i = 0; i < cssClasses.length; i++) {
        var cssClass = cssClasses[i]
            m = cssClass.match('^handle_cell_([0-9\_]*\-([0-9]*))$')
            
            if(m) {
                chain_str = m[1];
                index = parseInt(m[2], 10);
                
                return {
                    id_chain: chain_str.split('_').map(function(idstr) { return parseInt(idstr, 10); }),
                    sibling_index: index
                }
            }
        }
        console.log('not found');
        return [];
    }
    
    // export
    //Hierarchy = HH;
    
})();
