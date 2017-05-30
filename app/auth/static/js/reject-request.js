"use strict";

function rejectRequest(result){
    $("#delete-btn").html(result).attr("disabled", true);
}

function reject(evt) {
    evt.preventDefault();

    var formInput = {
        "user_y_id": $("#user-info").data("userid")
    };

    $.post("/reject-request/{{user_y_id}}",
           formInput,
           rejectRequest
           );
}

$("#reject-edit-form").on("submit", reject);