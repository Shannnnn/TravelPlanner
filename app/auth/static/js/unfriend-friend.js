"use strict";

function unfriendRequest(result){
    $("#unfriend-btn").html(result).attr("disabled", true);
}

function unfriend(evt) {
    evt.preventDefault();

    var formInput = {
        "user_b_id": $("#user-info").data("userid")
    };

    $.post("/unfriend/{{user_b_id}}",
           formInput,
           unfriendRequest
           );
}

$("#unfriend-friend-form").on("submit", unfriend);