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
                    console.log('series');
                    console.log(series);

                    setInterval(function () {
                        load_cpu_usage_graph_ajax().done(function(data) {
                            console.log('load data');
                            console.log(data[0]);
                            series.addPoint(data[0], true, true);
                        });
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
            data: load_cpu_usage_graph_ajax().done(function(data) {
                return data;
            })
        }]
    });
}

function load_cpu_usage_graph_ajax() {
	var server = $('input[name="hwaddr"]').val();
	var csrf = $('input[name="csrfmiddlewaretoken"]').val();
	var secret = $('input[name="secret"]').val();

	var address = '/ajax/server/' + server + '/metrics/cpu_usage/';

	return $.ajax({
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
		}
	});
}
