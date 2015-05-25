$.document.ready(function() {
	load.cpu_usage.graph.ajax('cpu_usage');
});

function load.cpu_usage.graph.ajax(identifier) {
	var server = $('input[name="hwaddr"]').val();

	var addres = '/ajax/server/' + server + '/metrics/cpu_usage'; 
	
	console.log('addres');
}
