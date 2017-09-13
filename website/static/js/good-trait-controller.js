function checkin(id) {

  event.preventDefault();
  if ($("#goodtraitcheckin-" + id).hasClass("good-notdone"))
  {
      $.ajax({
          url : "trait/good/checkin/" + id,
          type : "GET",
          datatype: 'json',
          success : function() {
            $("#goodtraitcheckin-"+id).toggleClass("good-done");
            $("#goodtraitcheckin-"+id).toggleClass("good-notdone");
            var goodFor = parseInt($("#goodfor-" + id).html()) + 1
            console.log(goodFor)
             $("#goodfor-" + id).text(goodFor)
          },
          error : function(xhr,errmsg,err) {
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }
      });
    } else {
      console.log("rolling back");
      event.preventDefault();
      $.ajax({
          url : "trait/good/undocheckin/" + id,
          type : "GET",
          datatype: 'json',
          success : function() {
            $("#goodtraitcheckin-"+id).toggleClass("good-done");
            $("#goodtraitcheckin-"+id).toggleClass("good-notdone");
            var goodFor = parseInt($("#goodfor-" + id).html()) - 1
            console.log(goodFor)
            $("#goodfor-" + id).text(goodFor)
          },
          error : function(xhr,errmsg,err) {
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }
      });
    }
};

function delete_good_trait(id) {
  event.preventDefault();
  $.ajax({
      url : "trait/good/delete/" + id,
      type : "GET",
      datatype: 'json',
      success : function(response) {
        location.reload();
        console.log(response);
      },
      error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  });
};
