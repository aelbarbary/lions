function actout(id) {
  event.preventDefault();
  $.ajax({
      url : "trait/bad/actout/" + id,
      type : "GET",
      datatype: 'json',
      success : function(response) {
        console.log(response.soberFor);
        $("#badtraitcheckin-"+id).toggleClass("done");
        $("#badtraitcheckin-"+id).toggleClass("notdone");
        $("#soberfor-" + id).text("for " + response.soberFor + " days")
      },
      error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  });
};


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
