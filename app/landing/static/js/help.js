function return_Result(){
    var res = $('input[name="searchbar"]').val();
    window.location.replace("/main/planned-trips/"+res);
}

//Newest Trips and Most popular
function state(tripname, from, to, views, image, userid){
      return   '<div id="able" value="'+tripname+'" data-filter="'+tripname+'">'+
      '<a href="/main/view/'+tripname+'" target="_blank">'+
      '<div class="col-sm-3 text-center">'+
                            '<div class="container" style="display:inline; width:100%;">'+
                                '<div class="panel panel-default bootcards-media" style="width:100%;">'+ 
                                    '<div class="panel-heading" align="left" style="width: 100%;">'+tripname+'</div>'+
                                    '<div class="panel-body" style="width: 270px; height: 125px;" align="center">'+
                                    '<img style="height: 110%; width: 110%; object-fit:contain;" src="/trips/static//images/users/'+userid+'/'+image+'"/></div>'+
                                    '<div class="panel-footer" align="left" style="display: inline-block; width: 100%;">'+
                                      '<div class="row">'+
                                            '&nbsp; From:'+from+
                                        '</div>'+
                                        '<div class="row">'+
                                            '&nbsp; To:'+to+
                                            '&nbsp; <p class="fa fa-eye" aria-hidden="true"></p> '+views+
                                        '</div>'+
                                    '</div>'+
                                '</div>'+
                            '</div>'+ 
                        '</div>'+'</a>'+'</div>';

}

function sendMail(){
      $.getJSON('/main/sendResponse', {
              name : $('input[name="resID"]').val(),
              email : $('input[name="resEMAIL"]').val(),
              body : $('textarea[name="resMSG"]').val()
            }, function(data) {
            $('input[name="resID"]').val('');
            $('input[name="resEMAIL"]').val('');
            $('textarea[name="resMSG"]').val('');
            if(data.sent==true){
              swal('Message Sent!');
            }
            else
              swal('An error occured!');
            
        });
        return false;
}

var cad = [1, true, 1, true];
var item = ["#res", 'a[name="new_next"]', "#res_1", 'a[name="most_next"]']

    function res(ch, kh){

      if((ch==0 && kh==0) || (ch==2 && kh==0)){
        if(cad[ch+1]==true)
           cad[ch]++;
        if(cad[ch]==1)
          cad[ch]++;
      }else if((ch==0 && kh==1) || (ch==2 && kh==1)){
        if(cad[ch]>1)
          cad[ch]--;
      }
        $.getJSON('/main/paginate/'+(ch+1), {
              page: cad[ch]
            }, function(data) {
            $(item[ch]).html("");
              var stringRes = "";
              if(data.determiner==false){
                cad[ch+1] = false;
                $(item[ch+1]).hide();
              }
              else if(data.determiner==true){
                $(item[ch+1]).show();
                cad[ch+1] = true;
              }

            for(i=0; i<data.size; i++){
                stringRes+=state(data.result1[i], JSON.stringify(data.result2[i]).slice(5,17), JSON.stringify(data.result3[i]).slice(5,17), data.result4[i], data.result5[i], data.result6[i]);
            }
            $(item[ch]).append(stringRes);
        });
        return false;
    }




function callit(num, text){
  $('#exampleModalLong').html("")
  Stringrespify = '<div class="modal-dialog" role="document" style="width: 1000px; height:500px;">'+
    '<div class="modal-content">'+
      '<div class="modal-header">'+
        '<h5 class="modal-title" id="exampleModalLongTitle">'+text+'</h5>'+
      '</div>'+
      '<div class="modal-body" style="width: 1000px; height: 700px;">'+
        '<img style="height: 100%; width: 100%; object-fit:contain;" src="/main/static//images/misc/'+num+'.jpg"/>'+
      '</div>'+
      '<div class="modal-footer">'+
        '<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>'+
      '</div>'+
    '</div>'+
  '</div>';

  $('#exampleModalLong').append(Stringrespify)
  $('#exampleModalLong').modal('show'); 
}


$('#filter_within').on('keyup', function(){
    $('div[data-filter]').hide();
   var txt = $('#filter_within').val();
   if(txt){
    $('div[data-filter]:contains("'+txt+'")').show();
    }else{
      $('div[data-filter]').show();
    }
});


function trips_plans(keyword, num){
      $.getJSON('/main/exp/'+keyword, {
              page : num,
            }, function(data) {
              $('#views_ly').html("");
              var stringRes = "";
              for(i=0; i<data.size; i++){
                stringRes+=state(data.result1[i], JSON.stringify(data.result2[i]).slice(5,17), JSON.stringify(data.result3[i]).slice(5,17), data.result4[i], data.result5[i], data.result6[i]);
            }
            $('#views_ly').append(stringRes);
        });
        return false;
}

function trips_plans_for_main_search(keyword, num){
      $.getJSON('/main/search_main_/'+keyword, {
              page : num,
            }, function(data) {
              $('#views_res').html("");
              var stringRes = "";
              for(i=0; i<data.size; i++){
                stringRes+=state(data.result1[i], JSON.stringify(data.result2[i]).slice(5,17), JSON.stringify(data.result3[i]).slice(5,17), data.result4[i], data.result5[i], data.result6[i]);
            }
            $('#views_res').append(stringRes);
        });
        return false;
}