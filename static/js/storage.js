function ajaxBlock() {
	if ($('#storage_datatable input:focus').length) return true;
	if ($('#storage_datatable select:focus').length) return true;
	return false;
}

function storageDataInit() {
	$('#storage_datatable .cloud_data').dataTable({
			'lengthMenu': [[10, 25, 50, 100, 250, 500, 1000], [10, 25, 50, 100, 250, 500, 1000]],
			'stateSave': true,
			'iDisplayLength': 25,
			});
}

function ajaxStorage() {
	if (ajaxBlock()) return;
	$.ajax({ url: "/ajax/cloud/storage/", type: "GET", dataType: "html", success: ajaxStorageUpdate });
}

function ajaxStorageUpdate(content) {
	if (ajaxBlock()) return;
	$('#storage_datatable').html(content);
	storageDataInit();
	// prevent moving to top
	$('a[href="#"][data-top!=true]').click(function(e){ e.preventDefault(); });

}

function thumbnailCheck(zone, file, ext, path) {
	var fExt = file.name.toLowerCase().substring(file.name.length - ext.length);
	if (fExt != ext) return false;
	zone.emit("thumbnail", file, path);
	return true;
}

function setupDropzone(zone) {
	if (zone == undefined) return;
	zone.on("addedfile", function(file) {
		// images already handled
		if (file.type.match(/image.*/)) return;
		// Okey, sem treba rovnako pridat dalsie typy. file.type je MIME, file.name je nazov
		if (thumbnailCheck(zone, file, ".txt", "/static/images/icon-todo.png")) return;
		if (thumbnailCheck(zone, file, ".wav", "/static/images/icon-todo.png")) return;
	});
}

$(document).ready (function() {
	storageDataInit();
	window.setInterval ( function() { ajaxStorage(); } , 2000);

	window.setTimeout( function() { setupDropzone(Dropzone.instances[0]); }, 500);
});

