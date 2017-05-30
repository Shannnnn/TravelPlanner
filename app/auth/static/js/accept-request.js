"use strict";

function acceptRequest(result){
    $("#accept-btn").html(result).attr("disabled", true);
}

function edit(evt) {
    evt.preventDefault();

    var formInput = {
        "user_y_id": $("#user-info").data("userid")
    };

    $.post("/accept-request/{{user_y_id}}",
           formInput,
           acceptRequest
           );
}

$("#accept-edit-form").on("submit", edit);