$(document).ready(function() {
	cpu_usage_fn();
});

function cpu_usage_fn() {
	$('#cpu_usage').highcharts({
		chart: {
            type: 'spline',
            events: {
                load: function() {
                    var series = this.series[0];

                    setInterval(function () {
                        var data = load_cpu_usage_graph_ajax();
                        series.addPoint([data[0][0], data[0][1]], true, true);
                    }, 2000);
                }
            }
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
            data: (load_cpu_usage_graph_ajax())()
        }]
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
			return data;
		}
	});

	return true;
}
