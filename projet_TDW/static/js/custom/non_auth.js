$("document").ready(function() {
  $("input").keypress(function() {
    $("#error").css("display", "block");
    $("#error").html(
      "Il semble que ne vous n'êtes pas connectés. Veuillez vous connecter ou vous inscrire pour pouvoir bénéficier d'une traduction"
    );
  });
});
