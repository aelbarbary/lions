var BookIt = BookIt || {};
BookIt.ProfileController = function () {
    this.$profilePage = null;
    this.$txtWelcome = null;
};

BookIt.ProfileController.prototype.init = function () {
    console.log("profile initialized");
    this.$profilePage = $("#page-profile");
    this.$txtWelcome = $("#text-welcome", this.$profilePage);
};

BookIt.ProfileController.prototype.onLoadCommand = function () {
  console.log(this.$txtWelcome);
  console.log("should set text welcome");
  this.$txtWelcome.html("Hello Abdlerhaman");
}
