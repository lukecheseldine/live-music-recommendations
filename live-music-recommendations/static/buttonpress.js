$(document).ready(function () {
  $("#One").click(function (e) {
    $("#Two").removeClass("active");
    $("#Three").removeClass("active");
  });

  $("#Two").click(function (e) {
    $("#One").removeClass("active");
    $("#Three").removeClass("active");
  });
  $("#Three").click(function (e) {
    $("#One").removeClass("active");
    $("#Two").removeClass("active");
  });
});
