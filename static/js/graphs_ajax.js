$(document).ready(function() {
	setInterval(cpu_usage_fn(), 2000);	
});

function cpu_usage_fn() {
	var data = load_cpu_usage_graph_ajax();
	
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
						(function () {
						console.log(data.responseText);	
						})
					]
			} 
		]
	});
}
	
function load_cpu_usage_graph_ajax() {
	var server = $('input[name="hwaddr"]').val();
	var csrf = $('input[name="csrfmiddlewaretoken"]').val();
	var secret = $('input[name="secret"]').val();

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
			return data;
		},
		error: function(data) {
			console.log(data.responseText);
			return data.responseText; 
		}
	});
			
	return true;
}
