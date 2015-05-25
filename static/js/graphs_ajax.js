$(document).ready(function() {
	cpu_usage_fn(cpu_usage);
});
function cpu_usage_fn(graph) {
	$('#cpu_usage').highcharts({
		chart: {
			type: 'spline'
		},
		title: {
			text: 'CPU Usage'
		},
		subtitle: {
			text: ''
		},
		xAxis: {
			type: 'datetime',
			title: {
				text: 'Datetime'
			}
		},
		yAxis: {
			title: {
				text: 'CPU %'
			},
		},
		min: 0,
		tooltip: {
			headerFormat: '<b>{series.name}:</b> {point.y:.2f}<br>',
			      pointFormat: '{point.x:%Y-%m-%d %H:%M:%S}'
			 },
		series: [{
			name: 'CPU Used',
			      	// Define the data points. All series have a dummy year
			      	// of 1970/71 in order to be compared on the same x axis. Note
			      	// that in JavaScript, months start at 0 for January, 1 for February etc.
			      	data: [
					setInterval(load_cpu_usage_graph_ajax(graph), 2000)
			      	]
			} 
		]
	});
}
	
function load_cpu_usage_graph_ajax(graph) {
	var server = $('input[name="hwaddr"]').val();
	var csrf = $('input[name="csrfmiddlewaretoken"]').val();
	var secret = $('input[name="secret"]').val();
	var graph = $('#cpu_usage');

	var address = '/ajax/server/' + server + '/metrics/cpu_usage/'; 

	$.ajax({
		url: address,
		type: 'POST',
		dataType: 'json',
		headers: {
			'X-CSRFToken': csrf
		},
		cache: false,
		data: {
			'server': server,
			'secret': secret
		},
		success: function(data) {
			console.log(data);
			return data;
		},
		error: function(data) {
			console.log(data);
			return false; 
		}
	});
			
	return true;
	console.log(address);
}
