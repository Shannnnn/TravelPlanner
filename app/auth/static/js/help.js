function change_table(id, username, email, firstname, lastname, role){
            var stringi='<td style="text-align: center"><a href="/admin/users/remove/'+username+'" class="btn btn-danger btn-xs" style="text-align: center"><span class="glyphicon glyphicon-trash"></span></a></td>';

            if(role=='Admin')
                stringi='<td style="text-align: center"><a class="btn btn-danger btn-xs" style="text-align: center" disabled readonly><span class="glyphicon glyphicon-trash"></span></a></td>';

            console.log('gothere');
            return '<tr>'+
                        '<td><a href="/admin/users/edit/'+username+'" class="btn btn-success btn-xs" style="text-align: center"><span class="glyphicon glyphicon-pencil"></span></a></td>'+
                        stringi+
                        '<td>'+id+'</td>'+
                        '<td>'+username+'</td>'+
                        '<td>'+email+'</td>'+
                        '<td>'+firstname+'</td>'+
                        '<td>'+lastname+'</td>'+
                        '<td>'+role+'</td>'+
                    '</tr>';
        }

 function user_tabbing(condition, num){
              $.getJSON('/admin/paginate/users/'+condition, {
                      page : num,
                    }, function(data) {
                      $('#userTab').html("");
                      var stringRes = "";
                      for(i=0; i<data.size; i++){
                        stringRes+=change_table(data.u_id[i], data.u_name[i], data.u_email[i], data.u_fname[i], data.u_lname[i], data.u_role[i]);
                    }
                    $('#userTab').append(stringRes);
                });
                return false;
        }


function trip_replace(tripName, tripFrom, tripTo, tripViews){
    return '<div>'+
                                    '<div class="col-sm-3 text-center">'+
                                    '<div class="container" style="display:inline; width:100%; lenght:100%">'+
                                    '<div class="panel panel-default bootcards-media" style="width:100%;">'+
                                    '<div class="panel-heading" align="center" style="width: 100%;">'+
                                        tripName+
                                    '</div>'+
                                        '<a href="/admin/trips/{{ trip.tripName }}/itineraries">'+
                                        '<div class="panel-body" style="width: 200px; height: 125px;" align="center">'+
                                            '<img style="height: 100%; width: 100%; object-fit:contain;" src="https://i.ytimg.com/vi/QGiJFumHUPo/maxresdefault.jpg"/>'+
                                        '</div>'+
                                        '</a>'+
                                    '<div class="panel-footer" align="left" style="display: inline-block; width: 100%;">'+
                                        '<div class="row">'+
                                            '&nbsp; From: '+tripFrom+
                                        '</div>'+
                                        '<div class="row">'+
                                            '&nbsp; To: '+tripTo+
                                            '<br>&nbsp; '+tripViews +'views'+
                                        '</div>'+
                                        '<div class="panel-footer">'+
                                            '<div class="row" align="center" style="display: inline-block; width: 120%;">'+
                                                '<a href="/admin/trips/'+tripName+'/itineraries" class="btn btn-primary" style="display: inline-block; width: 30%;"><span class="fa fa-bars"></span></a>'+
                                                '<a href="/admin/trips/edit/'+tripName+'" class="btn btn-success" style="display: inline-block; width: 30%;"><span class="fa fa-pencil"></span></a>'+
                                                '<a class="btn btn-danger" href="" style="display: inline-block; width: 30%;"><span class="fa fa-trash"></span></a>'+
                                            '</div>'+
                                        '</div>'+
                                    '</div>'+
                                '</div>'+
                           '</div>'+
                        '</div>'+
                        '</div>'+
                    '</div>';

}


function trip_tabbing(num){
              $.getJSON('/admin/paginate/trips', {
                      page : num,
                    }, function(data) {
                      $('#key_trip').html("");
                      var stringRes = "";
                      for(i=0; i<data.size; i++){
                        stringRes+=trip_replace(data.t_name[i], JSON.stringify(data.t_from[i]).slice(5,17), JSON.stringify(data.t_to[i]).slice(5,17), data.t_views[i]);
                    }
                    $('#key_trip').append(stringRes);
                });
                return false;
        }


function paginateThis(name, id, code){
                return '<tr>'+
                            '<td><a href="/admin/trips/location/edit/'+id+'" class="btn btn-success btn-xs" style="text-align: center"><span class="glyphicon glyphicon-pencil"></span></a></td>'+
                        '<td><a href="/admin/trips/location/remove/'+id+'" class="btn btn-danger btn-xs" style="text-align: center"><span class="glyphicon glyphicon-trash"></span></a></td>'+
                                            '<td>'+name+'</td>'+
                                            '<td>'+code+'</td>'+
                                            '<td style="text-align: center"><a href="/admin/trips/'+name+'/city" class="btn btn-primary btn-xs"><span class="glyphicon glyphicon-plus"></span></a></td>'+
                                        '</tr>';
            }

            function paginator_ic(num){
              $.getJSON('/paginate/trips/location', {
                      page : num,
                    }, function(data) {
                      var stringRes = "";
                      for(i=0; i<data.size; i++){
                        stringRes+=paginateThis(data.cnName[i], data.cnID[i], data.cnCode[i]);
                        console.log(data.cnName[i]);
                    }
                    $('#table-body').html("");
                    $('#table-body').append(stringRes);
                });
                return false;
        }

function paginateThisCity(name, id, code, countryName){
                return '<tr>'+
                            '<td style="text-align: center"><a href="/admin/trips/'+countryName+'/city/'+id+'/edit" class="btn btn-success btn-xs" style="text-align: center"><span class="glyphicon glyphicon-pencil"></span></a></td>'+
                            '<td style="text-align: center"><a href="/admin/trips/'+countryName+'/city/'+id+'/remove" class="btn btn-danger btn-xs" style="text-align: center"><span class="glyphicon glyphicon-trash"></span></a></td>'+
                            '<td>'+id+'</td>'+
                            '<td>'+name+'</td>'+
                            '<td>'+code+'</td>'+
                        '</tr>';
            }

            function paginator_ic_city(num, country){
              $.getJSON('/paginate/trips/location/cities/'+country, {
                      page : num,
                    }, function(data) {
                      var stringRes = "";
                      for(i=0; i<data.size; i++){
                        stringRes+=paginateThisCity(data.ctName[i], data.ctID[i], data.ctCode[i], data.cnName_);
                        console.log(data.cnName_);
                    }
                    $('#table-city').html("");
                    $('#table-city').append(stringRes);
                });
                return false;
        }
