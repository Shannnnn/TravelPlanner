"use strict";

function rejectRequest(result){
    $("#deleted-btn").html(result).attr("disabled", true);
}

function reject(evt) {
    evt.preventDefault();

    var formInput = {
        "user_b_id": $("#user-info").data("userid")
    };

    $.post("/reject-friend/{{user_b_id}}",
           formInput,
           rejectRequest
           );
}

$("#reject-friend-form").on("submit", reject);