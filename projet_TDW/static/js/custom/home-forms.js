$("document").ready(function() {
  $("#find_translator").click(function(e) {
    e.preventDefault();
    console.log(
      $("#src_language_select")
        .children("option:selected")
        .val()
    );
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
        sworn_in: $("#trans_check").is(":checked") ? "true" : "false"
      },
      success: function(response, textStatus, jqXHR) {
        $("#ajax_response").html(response);
        $("#submit_3").css("visibility", "visible");
        $(".translatorCheckbox").click(function() {
          let objs = $(".translatorCheckbox");
          let res = "";
          for (i = 0; i < objs.length; i++) {
            if ($("#" + objs[i].id).is(":checked"))
              res = res + $("#" + objs[i].id).attr("value") + " ";
          }

          $('input[name="translators"]').attr("value", res);
        });
      }
    });
  });
});
