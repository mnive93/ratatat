var ws,ws2,moz;
function activate_tornado() {
      function start_chat_ws() {
         ws = new SockJS("http://127.0.0.1:8888/track");
         ws2 = new SockJS("http://127.0.0.1:8888/comment");
         ws3 = new SockJS("http://127.0.0.1:8888/opinion");
         ws.onmessage = function(event) {
         var message_data = JSON.parse(event.data);
            var date = new Date(message_data.timestamp*1000);
            var time = $.map([date.getHours(), date.getMinutes(), date.getSeconds()], function(val, i) {
                return (val < 10) ? '0' + val : val;
        });
 };
        ws2.onmessage = function(event) {
        var message_data = JSON.parse(event.data);
            var id = message_data.post;
            var date = new Date(message_data.timestamp*1000);
          var time = $.map([date.getHours(), date.getMinutes(), date.getSeconds()], function(val, i) {
                return (val < 10) ? '0' + val : val;
        });
          var d = document.getElementById(id);
          var str = d.innerHTML;
          d.innerHTML= str+message_data.text+"<br/>";

      var textarea = $("textarea#id_content");
      textarea.val("");    

    //$(id).append('<div  class="span4 well post-wrapper"><h5 class="poster-name">'+ message_data.sender +'</h5><h6 class="post-time">' + time[0] + ':' + time[1] + ':' + time[2]  '</h6><p class="post-text">'+message_data.text +'</p></div>');
        

        
          }  
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

$("button#like").click(function(event)

 {
     
     like($(this).parent().find('input[id="post_id"]').val());
 });

$("button#dislike").click(function(event)

 {
     
     dislike($(this).parent().find('input[id="post_id"]').val());
 });
function like(post_id)
{
  if($('button#like').hasClass('btn-success'))
  {
$('button#like').removeClass('btn-success').addClass('btn-danger');
ws3.send(JSON.stringify({
  post_id: post_id,
  value:"1",
}));
  }
  else
  {
   $('button#like').removeClass('btn-danger').addClass('btn-success');
    ws3.send(JSON.stringify({
   post_id: post_id,
   value:"0",
    }));

  }
}
function like(post_id)
{
  if($('button#dislike').hasClass('btn-success'))
  {
$('button#like').removeClass('btn-success').addClass('btn-danger');
ws3.send(JSON.stringify({
  post_id: post_id,
  value:"-1",
}));
  }
  else
  {
   $('button#dislike').removeClass('btn-danger').addClass('btn-success');
    ws3.send(JSON.stringify({
   post_id: post_id,
   value:"0",
    }));

  }
}

function send_message() {
      var textarea = $("textarea#id_content");
        if (textarea.val() == "") {
            return false;
        }
        if (ws.readyState != WebSocket.OPEN) {
            alert(ws.readyState);
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
            alert(ws.readyState);
            return false;
        }
   ws2.send(JSON.stringify({
  post_id: post_id,
  comment:comment,
}));
}

}
    
