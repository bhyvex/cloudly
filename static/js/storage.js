var dTable;

function ajaxBlock() {
	if ($('#storage_datatable input:focus').length) 
		return true;
	if ($('#storage_datatable select:focus').length) 
		return true;
	return false;
}

function storageDataInit() {
	dTable = $('#storage_datatable .cloud_data').DataTable({
			'ajax': { 
				url: '/ajax/cloud/storage/'
			},
			'aLengthMenu': [[10, 25, 50, 100, 250, 500, 1000], [10, 25, 50, 100, 250, 500, 1000]],
			'iDisplayLength': 10,
			});
}

// =============================================================================
// =============================================================================
function ajaxStorage() {
	if (ajaxBlock()) 
		return;
	dTable.ajax.reload( function ( param ){
		$('.btn-pop').click(function(e){
			e.preventDefault();
			$('#myModal').modal('show');
		});
	}, false );
//	$.ajax({ url: "/ajax/cloud/storage/", type: "GET", dataType: "html", success: ajaxStorageUpdate });
}
// =============================================================================
// =============================================================================

function ajaxStorageUpdate(content) {
	if (ajaxBlock()) return;
	$('#storage_datatable .cloud_data').html(content);
	if (jQuery.fn.DataTable && jQuery.fn.DataTable.settings.length)
		jQuery.fn.DataTable.settings[0].nTable = $('#storage_datatable table');
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
		// add to the list: .sh, 
        if (thumbnailCheck(zone, file, ".3dm", "/static/file-icons/3dm.ico")) return;
        if (thumbnailCheck(zone, file, ".3ds", "/static/file-icons/3ds.ico")) return;
        if (thumbnailCheck(zone, file, ".3g2", "/static/file-icons/3g2.ico")) return;
        if (thumbnailCheck(zone, file, ".3gp", "/static/file-icons/3gp.ico")) return;
        if (thumbnailCheck(zone, file, ".7z", "/static/file-icons/7z.ico")) return;
        if (thumbnailCheck(zone, file, ".accdb", "/static/file-icons/accdb.ico")) return;
        if (thumbnailCheck(zone, file, ".ai", "/static/file-icons/ai.ico")) return;
        if (thumbnailCheck(zone, file, ".aif", "/static/file-icons/aif.ico")) return;
        if (thumbnailCheck(zone, file, ".apk", "/static/file-icons/apk.ico")) return;
        if (thumbnailCheck(zone, file, ".app", "/static/file-icons/app.ico")) return;
        if (thumbnailCheck(zone, file, ".asf", "/static/file-icons/asf.ico")) return;
        if (thumbnailCheck(zone, file, ".asp", "/static/file-icons/asp.ico")) return;
        if (thumbnailCheck(zone, file, ".aspx", "/static/file-icons/aspx.ico")) return;
        if (thumbnailCheck(zone, file, ".asx", "/static/file-icons/asx.ico")) return;
        if (thumbnailCheck(zone, file, ".avi", "/static/file-icons/avi.ico")) return;
        if (thumbnailCheck(zone, file, ".bak", "/static/file-icons/bak.ico")) return;
        if (thumbnailCheck(zone, file, ".bat", "/static/file-icons/bat.ico")) return;
        if (thumbnailCheck(zone, file, ".bin", "/static/file-icons/bin.ico")) return;
        if (thumbnailCheck(zone, file, ".bmp", "/static/file-icons/bmp.ico")) return;
        if (thumbnailCheck(zone, file, ".c", "/static/file-icons/c.ico")) return;
        if (thumbnailCheck(zone, file, ".cab", "/static/file-icons/cab.ico")) return;
        if (thumbnailCheck(zone, file, ".cbr", "/static/file-icons/cbr.ico")) return;
        if (thumbnailCheck(zone, file, ".cer", "/static/file-icons/cer.ico")) return;
        if (thumbnailCheck(zone, file, ".cfg", "/static/file-icons/cfg.ico")) return;
        if (thumbnailCheck(zone, file, ".cfm", "/static/file-icons/cfm.ico")) return;
        if (thumbnailCheck(zone, file, ".cgi", "/static/file-icons/cgi.ico")) return;
        if (thumbnailCheck(zone, file, ".class", "/static/file-icons/class.ico")) return;
        if (thumbnailCheck(zone, file, ".com", "/static/file-icons/com.ico")) return;
        if (thumbnailCheck(zone, file, ".cpl", "/static/file-icons/cpl.ico")) return;
        if (thumbnailCheck(zone, file, ".cpp", "/static/file-icons/cpp.ico")) return;
        if (thumbnailCheck(zone, file, ".crdownload", "/static/file-icons/crdownload.ico")) return;
        if (thumbnailCheck(zone, file, ".crx", "/static/file-icons/crx.ico")) return;
        if (thumbnailCheck(zone, file, ".cs", "/static/file-icons/cs.ico")) return;
        if (thumbnailCheck(zone, file, ".csr", "/static/file-icons/csr.ico")) return;
        if (thumbnailCheck(zone, file, ".css", "/static/file-icons/css.ico")) return;
        if (thumbnailCheck(zone, file, ".csv", "/static/file-icons/csv.ico")) return;
        if (thumbnailCheck(zone, file, ".cue", "/static/file-icons/cue.ico")) return;
        if (thumbnailCheck(zone, file, ".cur", "/static/file-icons/cur.ico")) return;
        if (thumbnailCheck(zone, file, ".dat", "/static/file-icons/dat.ico")) return;
        if (thumbnailCheck(zone, file, ".db", "/static/file-icons/db.ico")) return;
        if (thumbnailCheck(zone, file, ".dbf", "/static/file-icons/dbf.ico")) return;
        if (thumbnailCheck(zone, file, ".dds", "/static/file-icons/dds.ico")) return;
        if (thumbnailCheck(zone, file, ".deb", "/static/file-icons/deb.ico")) return;
        if (thumbnailCheck(zone, file, ".dem", "/static/file-icons/dem.ico")) return;
        if (thumbnailCheck(zone, file, ".deskthemepack", "/static/file-icons/deskthemepack.ico")) return;
        if (thumbnailCheck(zone, file, ".dll", "/static/file-icons/dll.ico")) return;
        if (thumbnailCheck(zone, file, ".dmg", "/static/file-icons/dmg.ico")) return;
        if (thumbnailCheck(zone, file, ".dmp", "/static/file-icons/dmp.ico")) return;
        if (thumbnailCheck(zone, file, ".doc", "/static/file-icons/doc.ico")) return;
        if (thumbnailCheck(zone, file, ".docx", "/static/file-icons/docx.ico")) return;
        if (thumbnailCheck(zone, file, ".drv", "/static/file-icons/drv.ico")) return;
        if (thumbnailCheck(zone, file, ".dtd", "/static/file-icons/dtd.ico")) return;
        if (thumbnailCheck(zone, file, ".dwg", "/static/file-icons/dwg.ico")) return;
        if (thumbnailCheck(zone, file, ".dxf", "/static/file-icons/dxf.ico")) return;
        if (thumbnailCheck(zone, file, ".eps", "/static/file-icons/eps.ico")) return;
        if (thumbnailCheck(zone, file, ".exe", "/static/file-icons/exe.ico")) return;
        if (thumbnailCheck(zone, file, ".fla", "/static/file-icons/fla.ico")) return;
        if (thumbnailCheck(zone, file, ".flv", "/static/file-icons/flv.ico")) return;
        if (thumbnailCheck(zone, file, ".fnt", "/static/file-icons/fnt.ico")) return;
        if (thumbnailCheck(zone, file, ".fon", "/static/file-icons/fon.ico")) return;
        if (thumbnailCheck(zone, file, ".gadget", "/static/file-icons/gadget.ico")) return;
        if (thumbnailCheck(zone, file, ".gam", "/static/file-icons/gam.ico")) return;
        if (thumbnailCheck(zone, file, ".gbr", "/static/file-icons/gbr.ico")) return;
        if (thumbnailCheck(zone, file, ".ged", "/static/file-icons/ged.ico")) return;
        if (thumbnailCheck(zone, file, ".gif", "/static/file-icons/gif.ico")) return;
        if (thumbnailCheck(zone, file, ".gpx", "/static/file-icons/gpx.ico")) return;
        if (thumbnailCheck(zone, file, ".gz", "/static/file-icons/gz.ico")) return;
        if (thumbnailCheck(zone, file, ".h", "/static/file-icons/h.ico")) return;
        if (thumbnailCheck(zone, file, ".hqx", "/static/file-icons/hqx.ico")) return;
        if (thumbnailCheck(zone, file, ".htm", "/static/file-icons/htm.ico")) return;
        if (thumbnailCheck(zone, file, ".html", "/static/file-icons/html.ico")) return;
        if (thumbnailCheck(zone, file, ".icns", "/static/file-icons/icns.ico")) return;
        if (thumbnailCheck(zone, file, ".ico", "/static/file-icons/ico.ico")) return;
        if (thumbnailCheck(zone, file, ".ics", "/static/file-icons/ics.ico")) return;
        if (thumbnailCheck(zone, file, ".iff", "/static/file-icons/iff.ico")) return;
        if (thumbnailCheck(zone, file, ".indd", "/static/file-icons/indd.ico")) return;
        if (thumbnailCheck(zone, file, ".ini", "/static/file-icons/ini.ico")) return;
        if (thumbnailCheck(zone, file, ".iso", "/static/file-icons/iso.ico")) return;
        if (thumbnailCheck(zone, file, ".jar", "/static/file-icons/jar.ico")) return;
        if (thumbnailCheck(zone, file, ".java", "/static/file-icons/java.ico")) return;
        if (thumbnailCheck(zone, file, ".jpg", "/static/file-icons/jpg.ico")) return;
        if (thumbnailCheck(zone, file, ".js", "/static/file-icons/js.ico")) return;
        if (thumbnailCheck(zone, file, ".jsp", "/static/file-icons/jsp.ico")) return;
        if (thumbnailCheck(zone, file, ".key", "/static/file-icons/key.ico")) return;
        if (thumbnailCheck(zone, file, ".keychain", "/static/file-icons/keychain.ico")) return;
        if (thumbnailCheck(zone, file, ".kml", "/static/file-icons/kml.ico")) return;
        if (thumbnailCheck(zone, file, ".kmz", "/static/file-icons/kmz.ico")) return;
        if (thumbnailCheck(zone, file, ".lnk", "/static/file-icons/lnk.ico")) return;
        if (thumbnailCheck(zone, file, ".log", "/static/file-icons/log.ico")) return;
        if (thumbnailCheck(zone, file, ".lua", "/static/file-icons/lua.ico")) return;
        if (thumbnailCheck(zone, file, ".m", "/static/file-icons/m.ico")) return;
        if (thumbnailCheck(zone, file, ".m3u", "/static/file-icons/m3u.ico")) return;
        if (thumbnailCheck(zone, file, ".m4a", "/static/file-icons/m4a.ico")) return;
        if (thumbnailCheck(zone, file, ".m4v", "/static/file-icons/m4v.ico")) return;
        if (thumbnailCheck(zone, file, ".max", "/static/file-icons/max.ico")) return;
        if (thumbnailCheck(zone, file, ".mdf", "/static/file-icons/mdf.ico")) return;
        if (thumbnailCheck(zone, file, ".mdb", "/static/file-icons/mdb.ico")) return;
        if (thumbnailCheck(zone, file, ".mid", "/static/file-icons/mid.ico")) return;
        if (thumbnailCheck(zone, file, ".mim", "/static/file-icons/mim.ico")) return;
        if (thumbnailCheck(zone, file, ".mov", "/static/file-icons/mov.ico")) return;
        if (thumbnailCheck(zone, file, ".mp3", "/static/file-icons/mp3.ico")) return;
        if (thumbnailCheck(zone, file, ".mp4", "/static/file-icons/mp4.ico")) return;
        if (thumbnailCheck(zone, file, ".mpa", "/static/file-icons/mpa.ico")) return;
        if (thumbnailCheck(zone, file, ".mpg", "/static/file-icons/mpg.ico")) return;
        if (thumbnailCheck(zone, file, ".msg", "/static/file-icons/msg.ico")) return;
        if (thumbnailCheck(zone, file, ".msi", "/static/file-icons/msi.ico")) return;
        if (thumbnailCheck(zone, file, ".nes", "/static/file-icons/nes.ico")) return;
        if (thumbnailCheck(zone, file, ".obj", "/static/file-icons/obj.ico")) return;
        if (thumbnailCheck(zone, file, ".otd", "/static/file-icons/otd.ico")) return;
        if (thumbnailCheck(zone, file, ".otf", "/static/file-icons/otf.ico")) return;
        if (thumbnailCheck(zone, file, ".pages", "/static/file-icons/pages.ico")) return;
        if (thumbnailCheck(zone, file, ".part", "/static/file-icons/part.ico")) return;
        if (thumbnailCheck(zone, file, ".pct", "/static/file-icons/pct.ico")) return;
        if (thumbnailCheck(zone, file, ".pdb", "/static/file-icons/pdb.ico")) return;
        if (thumbnailCheck(zone, file, ".pdf", "/static/file-icons/pdf.ico")) return;
        if (thumbnailCheck(zone, file, ".php", "/static/file-icons/php.ico")) return;
        if (thumbnailCheck(zone, file, ".pif", "/static/file-icons/pif.ico")) return;
        if (thumbnailCheck(zone, file, ".pkg", "/static/file-icons/pkg.ico")) return;
        if (thumbnailCheck(zone, file, ".pl", "/static/file-icons/pl.ico")) return;
        if (thumbnailCheck(zone, file, ".plugin", "/static/file-icons/plugin.ico")) return;
        if (thumbnailCheck(zone, file, ".png", "/static/file-icons/png.ico")) return;
        if (thumbnailCheck(zone, file, ".pps", "/static/file-icons/pps.ico")) return;
        if (thumbnailCheck(zone, file, ".ppt", "/static/file-icons/ppt.ico")) return;
        if (thumbnailCheck(zone, file, ".pptx", "/static/file-icons/pptx.ico")) return;
        if (thumbnailCheck(zone, file, ".prf", "/static/file-icons/prf.ico")) return;
        if (thumbnailCheck(zone, file, ".ps", "/static/file-icons/ps.ico")) return;
        if (thumbnailCheck(zone, file, ".psd", "/static/file-icons/psd.ico")) return;
        if (thumbnailCheck(zone, file, ".pspimage", "/static/file-icons/pspimage.ico")) return;
        if (thumbnailCheck(zone, file, ".py", "/static/file-icons/py.ico")) return;
        if (thumbnailCheck(zone, file, ".ra", "/static/file-icons/ra.ico")) return;
        if (thumbnailCheck(zone, file, ".rar", "/static/file-icons/rar.ico")) return;
        if (thumbnailCheck(zone, file, ".rm", "/static/file-icons/rm.ico")) return;
        if (thumbnailCheck(zone, file, ".rom", "/static/file-icons/rom.ico")) return;
        if (thumbnailCheck(zone, file, ".rpm", "/static/file-icons/rpm.ico")) return;
        if (thumbnailCheck(zone, file, ".rss", "/static/file-icons/rss.ico")) return;
        if (thumbnailCheck(zone, file, ".rtf", "/static/file-icons/rtf.ico")) return;
        if (thumbnailCheck(zone, file, ".sav", "/static/file-icons/sav.ico")) return;
        if (thumbnailCheck(zone, file, ".sdf", "/static/file-icons/sdf.ico")) return;
        if (thumbnailCheck(zone, file, ".sh", "/static/file-icons/sh.ico")) return;
        if (thumbnailCheck(zone, file, ".sitx", "/static/file-icons/sitx.ico")) return;
        if (thumbnailCheck(zone, file, ".sln", "/static/file-icons/sln.ico")) return;
        if (thumbnailCheck(zone, file, ".sql", "/static/file-icons/sql.ico")) return;
        if (thumbnailCheck(zone, file, ".srt", "/static/file-icons/srt.ico")) return;
        if (thumbnailCheck(zone, file, ".svg", "/static/file-icons/svg.ico")) return;
        if (thumbnailCheck(zone, file, ".swf", "/static/file-icons/swf.ico")) return;
        if (thumbnailCheck(zone, file, ".swift", "/static/file-icons/swift.ico")) return;
        if (thumbnailCheck(zone, file, ".sys", "/static/file-icons/sys.ico")) return;
        if (thumbnailCheck(zone, file, ".tar", "/static/file-icons/tar.ico")) return;
        if (thumbnailCheck(zone, file, ".tar.gz", "/static/file-icons/tar.gz.ico")) return;
        if (thumbnailCheck(zone, file, ".tax2012", "/static/file-icons/tax2012.ico")) return;
        if (thumbnailCheck(zone, file, ".tex", "/static/file-icons/tex.ico")) return;
        if (thumbnailCheck(zone, file, ".tga", "/static/file-icons/tga.ico")) return;
        if (thumbnailCheck(zone, file, ".thm", "/static/file-icons/thm.ico")) return;
        if (thumbnailCheck(zone, file, ".tif", "/static/file-icons/tif.ico")) return;
        if (thumbnailCheck(zone, file, ".tiff", "/static/file-icons/tiff.ico")) return;
        if (thumbnailCheck(zone, file, ".tmp", "/static/file-icons/tmp.ico")) return;
        if (thumbnailCheck(zone, file, ".toast", "/static/file-icons/toast.ico")) return;
        if (thumbnailCheck(zone, file, ".torrent", "/static/file-icons/torrent.ico")) return;
        if (thumbnailCheck(zone, file, ".ttf", "/static/file-icons/ttf.ico")) return;
        if (thumbnailCheck(zone, file, ".txt", "/static/file-icons/txt.ico")) return;
        if (thumbnailCheck(zone, file, ".uue", "/static/file-icons/uue.ico")) return;
        if (thumbnailCheck(zone, file, ".vb", "/static/file-icons/vb.ico")) return;
        if (thumbnailCheck(zone, file, ".vcd", "/static/file-icons/vcd.ico")) return;
        if (thumbnailCheck(zone, file, ".vcf", "/static/file-icons/vcf.ico")) return;
        if (thumbnailCheck(zone, file, ".vcxproj", "/static/file-icons/vcxproj.ico")) return;
        if (thumbnailCheck(zone, file, ".vob", "/static/file-icons/vob.ico")) return;
        if (thumbnailCheck(zone, file, ".wav", "/static/file-icons/wav.ico")) return;
        if (thumbnailCheck(zone, file, ".wma", "/static/file-icons/wma.ico")) return;
        if (thumbnailCheck(zone, file, ".wmv", "/static/file-icons/wmv.ico")) return;
        if (thumbnailCheck(zone, file, ".wpd", "/static/file-icons/wpd.ico")) return;
        if (thumbnailCheck(zone, file, ".wps", "/static/file-icons/wps.ico")) return;
        if (thumbnailCheck(zone, file, ".wsf", "/static/file-icons/wsf.ico")) return;
        if (thumbnailCheck(zone, file, ".xcodeproj", "/static/file-icons/xcodeproj.ico")) return;
        if (thumbnailCheck(zone, file, ".xhtml", "/static/file-icons/xhtml.ico")) return;
        if (thumbnailCheck(zone, file, ".xlr", "/static/file-icons/xlr.ico")) return;
        if (thumbnailCheck(zone, file, ".xls", "/static/file-icons/xls.ico")) return;
        if (thumbnailCheck(zone, file, ".xlsx", "/static/file-icons/xlsx.ico")) return;
        if (thumbnailCheck(zone, file, ".xml", "/static/file-icons/xml.ico")) return;
        if (thumbnailCheck(zone, file, ".yuv", "/static/file-icons/yuv.ico")) return;
        if (thumbnailCheck(zone, file, ".zip", "/static/file-icons/zip.ico")) return;
        if (thumbnailCheck(zone, file, ".zipx", "/static/file-icons/zipx.ico")) return;
	});
}

$(document).ready (function() {
	storageDataInit();
	window.setInterval ( function() { ajaxStorage(); } , 2000);

	window.setTimeout( function() { setupDropzone(Dropzone.instances[0]); }, 500);
});

