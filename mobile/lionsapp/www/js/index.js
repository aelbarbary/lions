var BookIt = BookIt || {};

// Begin boilerplate code generated with Cordova project.

var app = {
    // Application Constructor
    initialize: function () {
        this.bindEvents();
    },
    // Bind Event Listeners
    //
    // Bind any events that are required on startup. Common events are:
    // 'load', 'deviceready', 'offline', and 'online'.
    bindEvents: function () {
        document.addEventListener('deviceready', this.onDeviceReady, false);
    },
    // deviceready Event Handler
    //
    // The scope of 'this' is the event. In order to call the 'receivedEvent'
    // function, we must explicitly call 'app.receivedEvent(...);'
    onDeviceReady: function () {
        app.receivedEvent('deviceready');
    },
    // Update DOM on a Received Event
    receivedEvent: function (id) {

    }
};

app.initialize();

// End boilerplate code.

$(document).on("mobileinit", function (event, ui) {
    $.mobile.defaultPageTransition = "slide";
});

app.signupController = new BookIt.SignUpController();
app.signInController = new BookIt.SignInController();
app.profileController = new BookIt.ProfileController();

//$(document).delegate("#page-signup", "pagebeforeshow", function () {
//    // Reset the signup form.
//    app.signupController.resetSignUpForm();
//});

$(document).on("pagecontainerbeforechange", function (event, ui) {
    console.log("before chanhe");
    if (typeof ui.toPage !== "object") return;
    switch (ui.toPage.attr("id")) {
        case "page-index":
            console.log("page index");
            if (!ui.prevPage) {
                console.log("inside");
                // Check session.keepSignedIn and redirect to main menu.
                var session = BookIt.Session.getInstance().get(),
                    today = new Date();
                console.log(session);
                if (session && session.keepSignedIn && new Date(session.expirationDate).getTime() > today.getTime()) {
                      console.log("found session");
                      ui.toPage = $("#page-main-menu");
                }
            }
    }
});

$(document).on("pagecontainerbeforeshow", function (event, ui) {
    if (typeof ui.toPage == "object") {
        switch (ui.toPage.attr("id")) {
            case "page-signup":
                // Reset the signup form.
                app.signupController.resetSignUpForm();
                break;
            case "page-signin":
                // Reset signin form.
                console.log("signin clicked");
                app.signInController.resetSignInForm();
                break;
        }
    }
});

$(document).delegate("#page-signup", "pagebeforecreate", function () {

    app.signupController.init();

    app.signupController.$btnSubmit.off("tap").on("tap", function () {
        app.signupController.onSignupCommand();
    });

});

$(document).delegate("#page-signin", "pagebeforecreate", function () {
    console.log("user tries to log in");
    app.signInController.init();
    app.signInController.$btnSubmit.off("tap").on("tap", function () {
        app.signInController.onSignInCommand();
    });
});

$(document).delegate("#page-profile", "pageshow", function () {
    console.log("should show abdel name");
    app.profileController.init();
    app.profileController.onLoadCommand();
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
