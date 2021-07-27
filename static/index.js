function getBotResponse(){
    var myText = $("#my-text").val();
    var userBubble = '<div class="your-container"><div class="your-msg">'+ myText +'</div></div>';
    $("#my-text").val("");
    $(".chat-view").append(userBubble);
    $(".chat-view").stop().animate({scrollTop: $(".chat-view")[0].scrollHeight}, 1000);
    
    $.get("/get1", {msg: myText }).done(function(data){
        var a = data.payload;
        for (i = 0; i < a.length; i++) {
            if (a[i].hasOwnProperty("Text")) {
                var botBubble1 = '<div class="bot-container"><div class="bot-msg">'+ a[i].Text +'</div></div>';
                $(".chat-view").append(botBubble1);
            }
            if (a[i].hasOwnProperty("Image")) {
                var botBubble2 = '<img class="imgcard" src="' + a[i].Image + '" width="400" height="300">';
                $(".chat-view").append(botBubble2);
            }
            if (a[i].hasOwnProperty("Buttons")) {
                // alert("Buttons");
                // addSuggestion(response[i].Buttons);
                but = a[i].Buttons
                var suggLength = but.length;
                for (i = 0; i < suggLength; i++) {
                    var botBubble1 = '<div class="bot-container"><div class="bot-msg">'+ but[i].title +' '+ but[i].payload +'</div></div>';
                    $(".chat-view").append(botBubble1);
                    // $('<div class="menuChips" data-payload=\'' + (suggestions[i].payload) + '\'>' + suggestions[i].title + "</div>").appendTo(".menu");
                }
                // var botBubble2 = '<img class="imgcard" src="' + a[i].Image + '" width="400" height="300">';
                // $(".chat-view").append(botBubble2);
            }
        }
        // if (response[i].hasOwnProperty("image")) {
        //     var BotResponse = '<div class="singleCard">' + '<img class="imgcard" src="' + response[i].image + '">' + '</div><div class="clearfix">';
        //     $(BotResponse).appendTo(".chats").hide().fadeIn(1000);
        // }
        // var botBubble = '<div class="bot-container"><div class="bot-msg">'+ data.data +'</div></div>';
        // $(".chat-view").append(botBubble);
    }); 
}
$("#my-text").keypress(function(e){
    if (e.which == 13){
        getBotResponse();
    }
});

//====================================== Suggestions ===========================================

function addSuggestion(textToAdd) {
    setTimeout(function() {
        var suggestions = textToAdd;
        var suggLength = textToAdd.length;
        for (i = 0; i < suggLength; i++) {
            $('<div class="menuChips" data-payload=\'' + (suggestions[i].payload) + '\'>' + suggestions[i].title + "</div>").appendTo(".menu");
        }
        scrollToBottomOfResults();
    }, 1000);
}

// on click of suggestions, get the value and send to rasa
$(document).on("click", ".menu .menuChips", function() {
    var text = this.innerText;
    var payload = this.getAttribute('data-payload');
    console.log("payload: ", this.getAttribute('data-payload'))
    setUserResponse(text);
    send(payload);

    //delete the suggestions once user click on it
    $(".suggestions").remove();

});


// function getBotResponse(){
//     var myText = $("#my-text").val();
//     var userBubble = '<div class="your-container"><div class="your-msg">'+ myText +'</div></div>';
//     $("#my-text").val("");
//     $(".chat-view").append(userBubble);
//     $(".chat-view").stop().animate({scrollTop: $(".chat-view")[0].scrollHeight}, 1000);
    
//     $.get("/get", {msg: myText }).done(function(data){
//         var botBubble = '<div class="bot-container"><div class="bot-msg">'+ data +'</div></div>';
//         $(".chat-view").append(botBubble);
//     }); 
// }
// $("#my-text").keypress(function(e){
//     if (e.which == 13){
//         getBotResponse();
//     }
// });