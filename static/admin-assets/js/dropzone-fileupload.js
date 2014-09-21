$('#upload').fileupload({
  filesContainer: 'tbody.files',
  uploadTemplateId: null,
  downloadTemplateId: null,
  dataType: 'json',
  
  uploadTemplate: function(o){
      
      var rows = $();
      $.each(o.files, function(index, file){
        var tpl = $('<tr class="template-upload fade">'+
                          '<td align="center"><span class="preview"></span></td>'+
                          '<td class="filename"></td>'+
                          '<td class="filesize"></td>'+
                          '<td class="status"><div class="progress"></div></td>'+
                          '<td class="action">'+
                              (!index && !o.options.autoUpload ?
                              '<button class="btn btn-sm btn-primary start" disabled>Upload</button>' : '') +
                              (!index ? '<button class="btn btn-sm btn-warning cancel">Cancel</button>' : '')+
                          '</td>'+
                     '</tr>');
            
            tpl.find('td.filename').text(file.name);
            tpl.find('td.filesize').append('<i>'+formatFileSize(file.size)+'</i>');
            if(file.thumbnailUrl){
                tpl.find(".preview").append($("img").prop('src',file.thumbnailUrl));
            }
            rows = rows.add(tpl);
      });
      
      return rows;
      
  },
  downloadTemplate: function(o){
      var rows = $();
      $.each(o.files, function(index, file){
        var tpl = $('<tr class="template-download fade">'+
                          '<td align="center"><span class="preview"></span></td>'+
                          '<td class="filename"></td>'+
                          '<td class="filesize"></td>'+
                          '<td class="status"><span class="label label-warning">Synchronising..</span></td>'+
                          '<td class="action">'+
                              (!index && !o.options.autoUpload ?
                              '<button class="btn btn-sm btn-primary start" disabled>Upload</button>' : '') +
                              (!index ? '<button class="btn btn-sm btn-warning cancel">Cancel</button>' : '')+
                          '</td>'+
                     '</tr>');
            
            tpl.find('td.filename').text(file.name);
            tpl.find('td.filesize').append('<i>'+formatFileSize(file.size)+'</i>');
            if(file.thumbnailUrl){
                tpl.find(".preview").append($("img").prop('src',file.thumbnailUrl));
            }
            rows = rows.add(tpl);
      });
      
      return rows;
  },
  progressall: function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        $('#progressAll .progress-bar').css(
            'width',
            progress + '%'
        );
    }
  
});
//Helper function for calculation of progress
function formatFileSize(bytes) {
    if (typeof bytes !== 'number') {
        return '';
    }

    if (bytes >= 1000000000) {
        return (bytes / 1000000000).toFixed(2) + ' GB';
    }

    if (bytes >= 1000000) {
        return (bytes / 1000000).toFixed(2) + ' MB';
    }
    return (bytes / 1000).toFixed(2) + ' KB';
}