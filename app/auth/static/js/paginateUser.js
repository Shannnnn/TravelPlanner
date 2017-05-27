function returnUsers(fname, lname, address, city, cas, id, index){
    
    var prof = '<img class="avatar border-gray" src="/static//images/users/'+id+'/'+cas+'" alt="Image for '+fname+'" style="width:90px;height:90px;"/>';

    if(cas=='default')
        prof='<img class="avatar border-gray" src="{{current_user.gravatar(size=90)}}" alt="Image for'+fname+'"/>';

    return '<div class="col-xs-3 text-center">'+
                  '<div class="container">'+
                    '<div class="list-group">'+
                        '<a href="/users/'+id+'" class="list-group-item" style="width:230px;height:120px;">'+
                            '<div class="media">'+
                                '<div class="media-left">'+
                                    prof+
                                '</div><!-- /.media-left -->'+
                                '<div class="media-body">'+
                                    '<h3 class="media-heading">'+fname+' '+lname+'</h3>'+
                                    '<p>'+
                                        '<span class="glyphicon glyphicon-map-marker" aria-hidden="true"></span>'+
                                         'Location: '+address+', '+city+
                                    '</p>'+
                                    '</div><!-- /.media-body -->'+
                                  '</div><!-- /.media -->'+
                                '</a>'+
                              '</div><!-- /.list-group -->'+
                              '</div>'+
                            '</div><!-- /.col -->';
                            
}

function getUserFriends(num){
      $.getJSON('/paginateUserFriends', {
              page : num,
            }, function(data) {
              $('#frList').html("");
              var stringRes = "";
              for(i=0; i<data.size; i++){
                stringRes+=returnUsers(data.fname[i], data.lname[i], data.addr[i], data.ct[i], data.cas[i], data.id[i], i);
            }
            console.log(stringRes);
            $('#frList').html("");
            $('#frList').append(stringRes);
        });
        return false;
}