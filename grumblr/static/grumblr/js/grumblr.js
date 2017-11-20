
function populateListPost() {
    $.get("/grumblr/feed/get_posts")
      .done(function(data) {
          console.log(data)
          var list = $("#allposts");
          list.html('')
          getUpdates();
          for (var i = 0; i < data.posts.length; i++) {
              post = data.posts[i];
              var new_post = $(post.html);
              new_post.data("post-id", post.id);
              new_post.data("p.user",post.user);
              new_post.data("p.date",post.date);
              new_post.data("p.content",post.content)
              list.prepend(new_post);
              console.log(new_post)
          }
      });
}

function addPost(){
    var postBtn = $("#id_content");
    $.post("/grumblr/post")
      .done(function(data) {
          getUpdates();
          postBtn.val("").focus();
      });
}

function addComment(post_id){
    var commentBtn = $("#id_text"+post_id);
    $.post("/grumblr/comment/" + post_id, {comment: commentBtn.val()})
      .done(function(data) {
          getUpdates();
          commentBtn.val("").focus();
      });
}

function getUpdates() {
    var list = $("#allposts")
    $.get("/grumblr/feed/get_posts")
      .done(function(data) {
          for (var i = 0; i < data.posts.length; i++) {
              var post = data.posts[i];
              var new_post = $(post.html);
              new_post.data("p", post.id);
              list.prepend(new_post);
          }
          var all_posts = list.children("div.pin");
          for (var j = 0; j < all_posts.length; j++) {
              post = all_posts[j];
              updateComments(post.id);
          }
      });
}

function updateComments(id) {
    var list = $("#allcomments");
    $.get("/grumblr/feed/get_comments"+ "/" + id)
      .done(function(data) {
          for (var i = 0; i < data.comments.length; i++) {
              var comment = data.comments[i];
              var new_comment = $(comment.html);
              list.append(new_comment);
          }
      });
}



$(document).ready(function () {

  // Add event-handlers
  $("#postBtn").click(addPost);

  // Set up to-do list with initial DB items and DOM data
  populateListPost();
  $("#id_content").focus();

  // Periodically refresh to-do list every 5 seconds
  window.setInterval(getUpdates, 5000);

// CSRF set-up copied from Django docs
  function getCookie(name) {  
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});