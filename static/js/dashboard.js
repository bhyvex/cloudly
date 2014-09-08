
function filterMachines(f) {
	$('.machines-buttons .quick-button').removeClass('active');
	if (f != 'all') $('.machines-buttons .btn-'+f).addClass('active');
	if (f == 'all') f = '*';
	else f = '.'+f;
	$('.machines-list').isotope( { filter: f } );
}

$(document).ready (function() {
	$('.machines-list').isotope();

	var btns = ['all', 'offline', 'suspended', 'windows', 'linux', 'bsd', 'private'];
	for (var i = 0; i < btns.length; ++i) {
	    (function(){
		var type = btns[i];
		var btn = $('.machines-buttons .btn-'+type);
		btn.click(function() { filterMachines(type); });
	    })();
	}
});
