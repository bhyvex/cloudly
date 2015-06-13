$(function () {
	$(document).ready(function () {
		var server = $('input[name="hwaddr"]').val();
		var csrf = $('input[name="csrfmiddlewaretoken"]').val();
		var secret = $('input[name="secret"]').val();

		processes(csrf, server, secret);
	});
});

function processes(csrf, server, secret) {
	var address = '/ajax/server/' + server + '/metrics/processes/';

	$('#running_processes_table').dataTable({
		lengthMenu: [[15, 50, 100], [15, 50, 100]],
		order: [[ 2, "desc" ]],
		draw: 1,
		processing: true,
		serverSide: true,
		ajax: {
			url: address,
			type: 'POST',
			dataType: 'json',
			dataSrc: function(json) {
				var data = [];
				for (var i = 0; i < json.data.length; i++) {

					var user = '';
					if (json.data[i]['cpu']  > 50) {
						user += '<span class="label label-danger">';
					} else {
						user += '<span class="label label-success">';
					}
					user += json.data[i]['user'];
					user += '</span>';

					data.push([
						json.data[i]['pid'],
						user,
						json.data[i]['cpu'],
						json.data[i]['mem'],
						json.data[i]['command'][0]
							.replace('[','')
							.replace(']',''),
						json.data[i]['command'].join(' ')
							.replace('[','')
							.replace(']','')
					]);
				}
				console.log(data);
				return data;
			},
			headers: {
				'X-CSRFToken': csrf
			},
			cache: false,
			data: {
				'server': server,
				'secret': secret
			}
		}
	}); //dataTable function end
}
