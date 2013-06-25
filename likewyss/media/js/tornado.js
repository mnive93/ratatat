   var ws,ws2,button;
function activate_tornado() {
  alert("tornado");
  alert("here");
    function start_chat_ws() {
        ws = new WebSocket("ws://127.0.0.1:8888/track/");
        ws2 = new WebSocket("ws://127.0.0.1:8888/comment/");
        ws.onopen = function () {
       }
        ws.onmessage = function(event) {
        var message_data = JSON.parse(event.data);
            var date = new Date(message_data.timestamp*1000);
            var time = $.map([date.getHours(), date.getMinutes(), date.getSeconds()], function(val, i) {
                return (val < 10) ? '0' + val : val;
        });
          }
        ws2.onopen = function () {
       }
        ws2.onmessage = function(event) {
          alert("hereee on messaaggggeee");
        var message_data = JSON.parse(event.data);
         alert(message_data.sender);
         alert(message_data.text);
            var date = new Date(message_data.timestamp*1000);
            var time = $.map([date.getHours(), date.getMinutes(), date.getSeconds()], function(val, i) {
                return (val < 10) ? '0' + val : val;
        });
          }  
        //$("div#posting").append('<div  class="span4 well post-wrapper"><h5 class="poster-name">'+ message_data.sender +mess_recv+'</h5><h6 class="post-time">' + time[0] + ':' + time[1] + ':' + time[2]  '</h6><p class="post-text">'+message_data.text +'</p></div>');
            
            
        ws.onclose = function(){
            // Try to reconnect in 5 seconds
             setTimeout(function() {start_chat_ws()}, 5000);
          
    
        };
    }

    if ("WebSocket" in window) {
        start_chat_ws();
    } 


$("button#postbut").click(send_message);
$("button#comment").click(function(event)
 {
     
     send_comment($(this).parent().find('input[id="post_id"]').val(),$(this).parent().find('textarea').val());
 });      


function send_message() {
      var textarea = $("textarea#id_content");
        if (textarea.val() == "") {
            return false;
        }
        if (ws.readyState != WebSocket.OPEN) {
            alert("error")
            return false;
        }
        ws.send(textarea.val());
        textarea.val("");

}
function send_comment(post_id,comment)
{
        if (comment == "") {
            return false;
        }
   
       if (ws.readyState != WebSocket.OPEN) {
            alert("error")
            return false;
        }
   ws2.send(JSON.stringify({
  post_id: post_id,
  comment:comment,
}));
}
}
    
