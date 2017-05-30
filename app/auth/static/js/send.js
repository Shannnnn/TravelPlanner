"use strict";

function showRequest(result) {
    $("#send-btn").html(result).attr("disabled", true);
}

function sendEditRequest(evt) {
    evt.preventDefault();

    var formInput = {
        "user_y_id": $("#user-info").data("userid")
    };

    $.post("/send-request/{{user_b_id}}",
           formInput,
           showRequest
           );
}

$("#send-form").on("submit", sendEditRequest);