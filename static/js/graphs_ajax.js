$(function () {
	$(document).ready(function () {
		var server = $('input[name="hwaddr"]').val();
		var csrf = $('input[name="csrfmiddlewaretoken"]').val();
		var secret = $('input[name="secret"]').val();

		cpu_usage_set (csrf, server, secret);
//		loadavg_set (csrf, server, secret);
	});
});

function cpu_usage_set (csrf, server, secret) {
	var address = '/ajax/server/' + server + '/metrics/cpu_usage/';

	function requestCpuUsageData(series, csrf, server, secret) {
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
				if (typeof element === 'undefined') {
					var element = [1,1];
				}

				if (element[0] != data[0]) {
					series.addPoint(data[0], true, true);
				}

				element [0] = data [0];
			}
		});
	}

	function updateCpuUsageChart(series, csrf, server, secret) {
		setInterval(function() {
			requestCpuUsageData(series, csrf, server, secret);
		}, 1000);
	}

	Highcharts.setOptions({
		global: {
			useUTC: false
		}
	});

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
			var cpuUsageChart = new Highcharts.Chart({
				chart: {
					renderTo: 'cpu_usage',
					events: {
						load: function() {
							updateCpuUsageChart(this.series[0], csrf, server, secret);
						}
					}
				},
			title: {
				text: 'CPU Usage'
			},
			xAxis: {
				type: 'datetime',
				tickPixelInterval: 1000
			},
			yAxis: {
				title: {
					text: 'Value'
				},
			plotLines: [{
				value: 0,
				width: 1,
				color: '#808080'
			}]
			},
			tooltip: {
				formatter: function () {
					return '<b>' + this.series.name + '</b><br/>' +
						Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x*1000) + '<br/>' +
						Highcharts.numberFormat(this.y, 2);
				}
			},
			legend: {
				enabled: false
			},
			exporting: {
				enabled: false
			},
			series: [{
				name: '% CPU used',
				data: data.reverse()
			}]
			});
		}
	});
}

function loadavg_set (csrf, server, secret)
{
	/*
	function requestLoadAvgData(series, csrf, server, secret) {
		var address = '/ajax/server/' + server + '/metrics/loadavg/';
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
				if (typeof element === 'undefined') {
					var element = [null,null];
				}

				if (element[0] != data[0]) {
					series.addPoint(data[0], true, true);
				}

				element [0] = data [0];
			}
		});
	}

	function updateLoadAvgChart(series, csrf, server, secret) {
		setInterval(function() {
			requestLoadAvgData(series, csrf, server, secret);
		}, 1000);
	}

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
			var cpuUsageChart = new Highcharts.Chart({
				chart: {
					renderTo: 'cpu_usage',
			events: {
				load: function() {
					updateChart(this.series[0], csrf, server, secret);
				}
			}
				},
			title: {
				text: 'CPU Usage'
			},
			xAxis: {
				type: 'datetime',
			tickPixelInterval: 1000
			},
			yAxis: {
				title: {
					text: 'Value'
				},
			plotLines: [{
				value: 0,
				width: 1,
				color: '#808080'
			}]
			},
			tooltip: {
				formatter: function () {
					return '<b>' + this.series.name + '</b><br/>' +
						Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
						Highcharts.numberFormat(this.y, 2);
				}
			},
			legend: {
				enabled: false
			},
			exporting: {
				enabled: false
			},
			series: [{
				name: '%CPU Usage',
				data: data.reverse()
			}]
			});
		}
	});
	*/
}
