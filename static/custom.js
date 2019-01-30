
// Initialise Pusher
const pusher = new Pusher('92992f27c9efddd649df', {
  cluster: 'us2',
  encrypted: true
});

// Subscribe to movie_bot channel
const channel = pusher.subscribe('liberty');

// bind new_message event to movie_bot channel
channel.bind('new_message', function(data) {
// Append human message
$('.chat-container').append(`
    <div class="chat-message human-message">
        ${input_message}
    </div>
`)

// Append bot message
$('.chat-container').append(`
    <div class="chat-message offset-md-7 bot-message">
        ${data.message}
    </div>
`)
});

var counter = 1;


// helper method that takes message and posts to bot, then appends new bot message based on that data
function submit_message(message) {

  $.post( "/send_message", {
      message: message,
      socketId: pusher.connection.socket_id
  }, handle_response);

  function handle_response(data) {

    // scroll to bottom jQuery function
    var scrollToBottom = () => $('.chat-container').scrollTop($('.chat-container')[0].scrollHeight);

    console.log(data);
    console.log('data.message is: ' + data.message);
    console.log(counter);

    var y = data.key;
    y = JSON.stringify(y);
    console.log(y);

    var list = JSON.stringify(data.buttons);
    console.log(typeof data.buttons);
    console.log(typeof list);
    console.log(list);

//
//      for (i=0; i < list.length; i++) {
//        console.log(list[i]);
//      }

    // checks if data.list exists
    // try if below doesn't work
    //if (data.list !== null)
    if (y === 'true') {

      //alert("Yes")
      console.log('got to list message. data.key is ' + y);

      // test data list
      //var datalist = ['Disciplinary', 'Behavior', 'Benefits', 'General', 'Salary'];
      
      // Append initial container
      $(".chat-container").append(`
        <div class="chat-message bot-message">
          Pick a topic:
          <div class="menu-container">
            <div id="btn_cont_${counter}" class="button-container">
            </div>
          </div>
        </div>
      `);


      // iterate over each element in data and display them as buttons  
      $.each(data.buttons, function(index, element) {
        //$(".button-container").append(`
        $("#btn_cont_" + counter).append(`
          <button class="topic-btn">${element}</button>	
        `);  
      });

      counter++;

      scrollToBottom();

      // get the value form each btn click and submit it to the function
      $(".topic-btn").on("click", function() {

        // gets the contents of the specified button sets it to value var
        var value = $(this).html(); 
        
        // Appends the value to new human message
        $(".chat-container").append(`
          <div class="chat-message human-message">
            ${value}
          </div>
        `);

        // here we should do a call to backend to make data.key to false
        // also dynamic id's for each chat message would be nice

        // submit value through submit function
        submit_message(value)

      });
      

    }

    else {

      // this is the default message without list parameter

      console.log(data.message);
      $('.chat-container').append(`
          <div class="chat-message bot-message">
              ${data.message}
          </div>
      `)
      // remove the loading indicator
      $( "#loading" ).remove();
    }
  }
}

// this is when form submission is made
$('#target').on('submit', function(e){
e.preventDefault();
const input_message = $('#input_message').val()
// return if the user does not enter any text
if (!input_message) {
  return
}

$('.chat-container').append(`
    <div class="chat-message human-message">
        ${input_message}
    </div>
`)

// loading
$('.chat-container').append(`
    <div class="chat-message text-center bot-message" id="loading">
        <b>...</b>
    </div>
`)

// clear the text input
$('#input_message').val('')

// send the message
submit_message(input_message)
});
