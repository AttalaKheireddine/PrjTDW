$("document").ready(function() {
  $("#find_translator").click(function(e) {
    e.preventDefault();
    $.ajax({
      type: "GET",
      url: "/select-translators",
      data: {
        src_language: $("#src_language_select")
          .children("option:selected")
          .val(),
        dest_language: $("#dest_language_select")
          .children("option:selected")
          .val(),
        category: $("#category_select")
          .children("option:selected")
          .val(),
        sworn_in: $("#trans_check").val()
      },
      success: function(response, textStatus, jqXHR) {
        $("#ajax_response").html(response);
        $("#submit_3").css("visibility", "visible");
        $("#submit_3").html(
          "Il semble que ne vous êtes pas connectés. Veuillez vous connecter ou vous inscrire pour pouvoir bénéficier d'une traduction"
        );
      }
    });
  });
});
