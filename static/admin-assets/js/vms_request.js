var vmsRequest = {
	interval: 2000,
	hasResponse: false,
	firstRun: true,
        callbacks: new Array(),
        callBackId: 0,
	initAction: function(){
		var $this = this;
		setInterval(function(){
			
			if($this.hasResponse === true || $this.firstRun === true){
				$this.firstRun = false;
				$this.hasResponse = false;
				$this.start();
			}
			
		},$this.interval);
	},
	start: function(){
		var $this = this;
		$.ajax({
			type: 'GET',
			url: '/ajax/cloud/vms/refresh/',
			data: 'nodata=nodata',
			success:function(res){
				if(res.indexOf('ALLDONE') !== -1){
					$this.hasResponse = true;
                                        $.each($this.callbacks,function(key,callback){
                                            if(callback && typeof(callback) === 'function'){
                                                callback();
                                            }                                           
                                        });
				}
			}
		});
	},
        addAfterStartHandler: function(callback){
            this.callBackId++;
            this.callbacks[this.callBackId] = callback;
        }
        
}
