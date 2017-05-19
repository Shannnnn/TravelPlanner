"use strict";

function acceptRequest(result){
    $("#accepted-btn").html(result).attr("disabled", true);
}

function friends(evt) {
    evt.preventDefault();

    var formInput = {
        "user_b_id": $("#user-info").data("userid")
    };

    $.post("/accept-friend/{{user_b_id}}",
           formInput,
           acceptRequest
           );
}

$("#accept-friend-form").on("submit", friends);