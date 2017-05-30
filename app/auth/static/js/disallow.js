"use strict";

function disallowRequest(result){
    $("#disallow-btn").html(result).attr("disabled", true);
}

function disallow(evt) {
    evt.preventDefault();

    var formInput = {
        "user_y_id": $("#user-info").data("userid")
    };

    $.post("/disallow/{{user_y_id}}",
           formInput,
           disallowRequest
           );
}

$("#disallow-form").on("submit", disallow);