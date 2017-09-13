function actout(id) {
  event.preventDefault();
  if ($("#badtraitactout-" + id).hasClass("bad-notdone"))
  {
    $.ajax({
        url : "trait/bad/actout/" + id,
        type : "GET",
        datatype: 'json',
        success : function(response) {
          console.log(response.soberFor);
          $("#badtraitcheckin-"+id).toggleClass("done");
          $("#badtraitcheckin-"+id).toggleClass("notdone");
          var soberFor = parseInt($("#sober-" + id).html()) + 1
          console.log(soberFor)
          $("#sober-" + id).text(soberFor)

        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
  } else {
    console.log("rolling back");
    event.preventDefault();
    $.ajax({
        url : "trait/bad/undoactout/" + id,
        type : "GET",
        datatype: 'json',
        success : function() {
          $("#badtraitcheckin-"+id).toggleClass("done");
          $("#badtraitcheckin-"+id).toggleClass("notdone");
          var soberFor = parseInt($("#sober-" + id).html()) + 1
          console.log(soberFor)
          $("#sober-" + id).text(soberFor)
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
  }

}


function delete_bad_trait(id) {
  event.preventDefault();
  $.ajax({
      url : "trait/bad/delete/" + id,
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
