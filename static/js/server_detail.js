$(document).ready(function() {
    $('#diskGraphs').deactivePanel();
    $('#serviceDiscovery').deactivePanel();
    $('#serverActivity').deactivePanel();
});

(function($) { 
    $.fn.deactivePanel = function() {
        this    
            .find('.btn-minimize')
            .find('i')
            .attr('class','fa fa-chevron-down');

        this
            .find('.panel-body')
            .css('display','none');
    };
})(jQuery);
