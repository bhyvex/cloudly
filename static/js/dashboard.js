
function filterMachines(f) {
	$('.machines-buttons .quick-button').removeClass('active');
	$('.machines-buttons .btn-'+f).addClass('active');
	if (f === 'all') f = '*';
	else f = '.'+f;
	$('#machines-loader').isotope( { filter: f } );
}

var cloudlyVMSmanager  = {
    template: '',
    actualMachines: '',
    colors : ['lightBlue','green','darkGreen','yellow','orange','red', 'silver'],
    initAction: function(){
        var $this = this;
        $('#machines-loader').isotope({
            itemSelector: '.vms-machine'
        });
        $.ajax({
            type: 'GET',
            url: '/ajax/cloud/box-template/',
            data: '',
            success: function(res){
                $this.template = res;
                setInterval(function(){
                    $this.loadMachinesData();
                },1000);
            }
        });
    },
    loadMachinesData: function(){ 
        var actualMachines = $(".vms-machine");
        
        var $this = this;
        $.ajax({
            type: 'GET',
            url: '/ajax/cloud/vms/',
            data: '',
            success: function(res){                
                var jsonData = $.parseJSON(res);
                $this.checkRemoved(jsonData,actualMachines);
                $this.parseMachinesData(jsonData);
                
            }
        });
    },
    parseMachinesData: function(jsonData){
        var $this = this;
        if(jsonData){
            $.each(jsonData,function(vms,data){
                //exist VMS
                if($('#'+vms).length){
                    $this.updateVMS(vms,data);
                }
                else {
                    $this.addVMS(vms,data);
                }
            });
        }
    },
    updateVMS: function(vms,data){
        chartStatElement($('#'+vms).find('.chart').html(data.averge));
        $('#'+vms).find('.value').html(data.state);

		var panel = $("#"+vms).find('.panel');
		$.each(this.colors,function(index,color){
			if(panel.hasClass(color) && panel.attr('class').indexOf(data.vmcolor) === -1){
				$(panel).switchClass(color,data.vmcolor,500,"easeInOutQuad");
				//console.log('VM '+vms+' changed color: '+color+' to: '+data.vmcolor+' and actual has class: '+panel.attr('class'));
				return;
			}
		}); 
		
    },
    addVMS: function(vms,data){
        var template = this.template;
        template = template.replace('{@vm@}',vms);
        template = template.replace('{@vm@}',vms);
        template = template.replace('{@vm@}',vms);
        template = template.replace('{@vmtitle@}',data.vmtitle);
        template = template.replace('{@vmcolor@}',data.vmcolor);
        template = template.replace('{@averge@}',data.averge);
        template = template.replace("{@state@}", data.state); 
        
        template = $(template);
//        console.log(template);
        var prepend = $('#machines-loader').prepend(template);
        chartStatElement($('#'+vms).find('.chart').html(data.averge));
        prepend.isotope( 'reloadItems' ).isotope({ sortBy: 'original-order' });
        
        
    },
    checkRemoved: function(machines,actualMachines){
        var machineIds = 'testVMS';
        $.each(machines,function(vms,value){
            machineIds += vms+',';
        });
        
        $.each(actualMachines,function(index,item){
            var id = $(item).attr('id');
            if(machineIds.indexOf(id) < 0){
                $('#'+id).fadeOut(500,'easeInOutQuart',function(){
                    $(this).remove();
                });
            }
        });
    },
    addBlank: function(){
        this.addVMS('testVMS',{"averge":"0.0,0.0,0.0,0.0","state":"Running"});
    
    }
}

$(document).ready (function() {
	
	var btns = ['all','critical','offline', 'suspended', 'windows', 'linux', 'bsd', 'private'];
	for (var i = 0; i < btns.length; ++i) {
	    (function(){
		var type = btns[i];
		var btn = $('.machines-buttons .btn-'+type);
		btn.click(function() { filterMachines(type); });
	    })();
	}
        
        cloudlyVMSmanager.initAction();
        
});


