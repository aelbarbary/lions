function loadSearchTerm(searchTerm)
{
  $('#s').val(searchTerm);
  search(searchTerm);
}

function updateSearchTerm() {
  resetSearchForm()

  var url = document.location.protocol + "//" + document.location.host + "/?q=";
  console.log(url);
  url += $('#s').val();
  window.history.pushState("object or string", "Title", url);
  search();
}

function search() {
  var searchTerm = $('#s').val();
  console.log("searchTerm:" + searchTerm);
  if (searchTerm == "")
  {
    $('#intro').show();
    return;
  }
  event.preventDefault();

  page = parseInt($('#pagination-id').val());
  $('#loadMore').prop("disabled", true);
  $('#loadMore').text("Loading ...");

  console.log("page:" + page);
  var data = {
    searchTerm : searchTerm,
    page: page
  };
  $.ajax({
      url : "search/", // the endpoint
      type : "POST", // http method
      data : JSON.stringify(data),
      success : function(json) {
        console.log("searching");
        var searchResults = document.getElementById('searchResults');
        // $('#searchResults').empty();
        $('#intro').hide();
        json.forEach(function(hit) {
            hit.fields.value = urlify(hit.fields.value);
            $("#searchTemplate").tmpl(hit).appendTo("#searchResults");
        });
        if(json.length < 10)
        {
            $('#loadMore').hide();
        }
        else {
            $('#loadMore').show();
            $('#loadMore').text("Load more");
            $('#loadMore').prop("disabled", false);
            $('#pagination-id').val(page + 1);
        }

      },
      error : function(xhr,errmsg,err) {
          $('#loadMore').text("No more data");
          $('#loadMore').prop("disabled", true);
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  });
};

function resetSearchForm()
{
  $('#searchResults').empty();
  $('#pagination-id').val(1);
  $('#pagination-id').val(1);
  $('#loadMore').text("Load more");
  $('#loadMore').prop("disabled", false);
}

function urlify(text) {
    var urlRegex = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)/;
    return text.replace(urlRegex, function(url) {
        return '<a href="' + url + '">' + url + '</a>';
    })
    // or alternatively
    // return text.replace(urlRegex, '<a href="$1">$1</a>')
}

function like(id) {
  event.preventDefault();
  $.ajax({
      url : "like/" + id,
      type : "GET",
      datatype: 'json',
      success : function(likes) {

        $("#likes-" + id).text(likes);
        $("#thumbs-up-" + id).toggleClass('liked disliked');
      },
      error : function(xhr,errmsg,err) {
          $('#answer-error-' + id).show();
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  });
};

$(function() {
    // This function gets cookie with a given name
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

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});
