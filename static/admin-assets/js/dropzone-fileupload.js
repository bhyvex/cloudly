$('#upload').fileupload({
  filesContainer: 'tbody.files',
  uploadTemplateId: null,
  downloadTemplateId: null,
  dataType: 'json',
  limitConcurrentUploads: 3,
  uploadTemplate: function(o){
      
      var rows = $();
      $.each(o.files, function(index, file){
        var fileId = hex_md5(file.name+file.size);
        var tpl = $('<tr id="'+fileId+'" class="template-upload fade">'+
                          '<td align="center"><span class="preview"></span></td>'+
                          '<td class="filename"></td>'+
                          '<td class="filesize"></td>'+
                          '<td class="status"><div class="progress"><span class="progressCount">0%</span><div class="progress-bar progress-bar-success" style="width:0%;"></div></div></td>'+
                          '<td class="action">'+
                              (!index && !o.options.autoUpload ?
                              '<button class="btn btn-sm btn-primary start start-btn" disabled>Upload</button>' : '') +
                              (!index ? '<button class="btn btn-sm btn-warning cancel cancel-btn">Cancel</button>' : '')+
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
                          '<td align="center"><span class="prev'+index+' preview"></span></td>'+
                          '<td class="filename"></td>'+
                          '<td class="filesize"></td>'+
                          '<td class="status"><span class="label label-warning">Synchronising..</span></td>'+
                          '<td class="action">'+
                              (!index && !o.options.autoUpload ?
                              '<button class="btn btn-sm btn-primary start start-btn" disabled>Upload</button>' : '') +
                              (!index ? '<button class="btn btn-sm btn-warning cancel cancel-btn">Cancel</button>' : '')+
                          '</td>'+
                     '</tr>');
            
            
            tpl.find('td.filename').text(file.name);
            tpl.find('td.filesize').append('<i>'+formatFileSize(parseInt(file.size))+'</i>');
            
            if(file.thumbnailUrl){
                var imgTag = $("<img>");
                imgTag.prop('src',file.thumbnailUrl);
                imgTag.prop('width','80');
                tpl.find(".preview").html(imgTag);
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

        $("#progressAll span.progressCount").text(progress+"%");
    },
  progress: function(e, data){
      var file = data.files[0];
      var fileId = hex_md5(file.name+file.size);
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var element = $("#"+fileId);
      element.find('.progress-bar').css('width', progress+'%');
      element.find(".progress span.progressCount").text(progress+'%');
      
      if(progress >= 100){
          element.find('.progress').fadeOut();
          var loader = $("<img>");
          loader.prop('src','/static/images/loading.gif');
          loader.prop('width','25');
          
          element.find('td.status').css("text-align","center").html(loader);
          
      }
  }  
  
});


    $("#startUpload").click(function(){
        var start = 0;
        $.each($('.start'),function(index,btn){
            start += 500;
            setTimeout(function(){$(btn).click();},start);
            
        });
    });
    
    $("#cancelUpload").click(function(){
        $('.cancel-btn').click();
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