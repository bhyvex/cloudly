
var cloudlyVMSmanager  = {
    template: '',
    actualMachines: '',
    colors: {
		'#36a9e1':'lightBlue',
		'#78cd51':'green',
		'#333366':'darkGreen',
		'#eae874':'yellow',
		'#fa603d':'lightOrange',
		'#ff5454':'red',
		'#CBD4E4':'silver',
		'#e84c8a':'pink',
		'#000000':'black'
    },
    tagMenuLink: null,
    tagMenuBox: null,
    tags: {},
    createTags: function() {
        var $this = this,
            serversTagsInput = $('input[name="available_servers_tags"]'),
            serversTags = serversTagsInput.val();

        serversTagsInput.remove();
        serversTags = serversTags
            .replace("]", "")
            .replace("[", "")
            .replace(/"/g, "")
            .replace(/ /g, "")
            .replace(/ /g, "")
            .split(",");

        for (i = 0; i < serversTags.length; i++) {
            serversTags[i] = serversTags[i]
                .trim()
                .replace(/\./g, "-");
        }
        this.tags = serversTags;
        this.tagMenuLink = $('.machines-buttons').find('.tag_selector');
        this.tagMenuBox = $('.machines-buttons').find('.tags-box');

        this.tagMenuLink.click(function() {
            $this.tagMenuLink.toggleClass('active');
            $this.tagMenuBox.slideToggle(200);
        });
    },
    bindClickTagAction: function () {
        var $this = this;

        var machinesButtons = $('.machines-buttons');
        for (var i = 0; i < $this.tags.length; ++i) {
            (function() {
                var type = $this.tags[i];
                var btn = machinesButtons.find('.btn-'+type);
                btn.click(function() {
                    $this.filterMachines(type);
                    $this.tagMenuLink.removeClass('active');
                    $this.tagMenuBox.hide();
                });
            })();
        }
    },
    filterMachines: function(f) {
        $('.machines-buttons .secondmenu-button').removeClass('active');
        $('.machines-buttons .btn-'+f).addClass('active');

        if (f === 'all') {
            f = '*';
        } else {
            f = '.'+f;
        }

        $('#machines-loader').isotope( { filter: f } );
    },
    initAction: function(){
        var $this = this;
        this.createTags();
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
                $this.bindClickTagAction();
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

        $.each(this.colors, function(code,color) {
            var $machine = $('#' + vms),
                panel = $machine.find('.panel');

            if(panel.hasClass(color) && panel.attr('class').indexOf(data.vmcolor) === -1) {
                var newClasses = 'vms-machine col-lg-3 col-md-6 ' + data.vmtitle;
                $machine.removeClass();
                $machine.addClass(newClasses);
                $(panel).removeClass(color).addClass(data.vmcolor)
                return;
            }
        });
    },
    addVMS: function(vms,data){
        var template = this.template;
        template = template.replace('{@vmlink@}',data.link);
        template = template.replace('{@vm@}',vms);
        template = template.replace('{@server@}',data.vmname);
        template = template.replace('{@vmtitle@}',data.vmtitle);
        template = template.replace('{@vmcolor@}',data.vmcolor);
        template = template.replace('{@averge@}',data.averge);
        template = template.replace("{@state@}", data.state);

        template = $(template);
        //console.log(template);
        var prepend = $('#machines-loader').prepend(template);
        chartStatElement($('#'+vms).find('.chart').html(data.averge));
        prepend.isotope( 'reloadItems' ).isotope({ sortBy: 'original-order' });
    },
    checkRemoved: function(machines,actualMachines){
        var machineIds = 'testVMS';
        var $container = $('#machines-loader');
        $.each(machines,function(vms,value){
            machineIds += vms+',';
        });
        $.each(actualMachines,function(index,item){
            var id = $(item).attr('id');
            if(machineIds.indexOf(id) < 0){
                $container.isotope( 'remove', item ).isotope('layout');
            }
        });
    },
    reloadPositions: function(){
            $('#machines-loader').isotope( 'reloadItems' ).isotope({ sortBy: 'original-order' });
    },
    addBlank: function(){
        this.addVMS('testVMS',{"averge":"0.0,0.0,0.0,0.0","state":"Running"});
    }
}

$(document).ready (function() {
    cloudlyVMSmanager.initAction();
});

