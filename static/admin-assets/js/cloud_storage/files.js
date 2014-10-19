var cloudlyFiles = {
	items: new Array(),
	currentItem: 0,
	currentAction: '',
	initAction: function(){
		var $this = this;
		
		$(document).ready(function(){
			$('.btn-pop').live('click',function(e){
			 	e.preventDefault();
				
				$this.currentAction = $(this).attr('rel');
				
				var itemId = $(this).parent().find('.fieldId').val(); 
				
				$("#myModal").find('.modal-body p').text('Item id is> '+itemId);
						
			});
		});
	},
	sendRequest: function(id){
		var $this = this;
		this.currentItem = id;
		
		$.ajax({
			url: '/ajax/cloud/storage/load-item/',
			type: 'GET',
			data: 'id='+id,
			success: function(res){
				var jsonData = $.parseJSON(res);
				$this.proccessResponse(jsonData);
			},
			error: function(res){
				if(res.type !== 200){
					$this.showErrorMessage();
				}
			}
		});
	},
	proccessResponse: function(res){
		this.items[this.currentItem] = new Array();		
		this.items[this.currentItem]['zoom'] 		= res.zoom;
		this.items[this.currentItem]['download']	= res.download;
		this.items[this.currentItem]['share']		= res.share;
		this.items[this.currentItem]['delete']		= res.deleteItem;
		
		this.showInfoBlock();
	},
	pasteDataToBlock: function(){
		var action = this.currentAction;
		var htmlData = this.items[this.currentItem][action];
		
	},
	showInfoBlock: function(){
		$('#myModal').modal('show');
	},
	showErrorMessage: function(){
			$("#myModal").find('.modal-body p').text('There is a problem with server, please try repeat the action again later.');
			this.showInfoBlock();
	}
}