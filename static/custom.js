// erics_branch
// Most of this is defaults from the project, still need a data.buttons from the back end

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


// helper method that takes message and posts to bot, then appends new bot message based on that data
function submit_message(message) {

    $.post( "/send_message", {
        message: message,
        socketId: pusher.connection.socket_id
    }, handle_response);

    function handle_response(data) {

      console.log(data.message);

      // checks if data.list exists
      // try if below doesn't work
      //if (data.list !== null)
      if (typeof data !== 'undefined') {
        console.log('got to list message');
        
        // Append initial container
        $(".chat-container").append(`
          <div class="chat-message bot-message">
            Pick a topic:
            <div class="menu-container">
              <div class="button-container"></div>
            </div>
          </div>
        `);

        // iterate over each element in data and display them as buttons  
        $.each(data, function(index, element) {
          $(".button-container").append(`
            <button class="topic-btn">${element.name}</button>	
          `);  
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
