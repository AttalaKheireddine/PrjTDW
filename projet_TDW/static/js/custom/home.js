$("document").ready(function() {
  $("#myBtn1").click(function() {
    more_less("myBtn1");
  });
  $("#myBtn2").click(function() {
    more_less("myBtn2");
  });
  $("#myBtn3").click(function() {
    more_less("myBtn3");
  });
});

function more_less(buttonId) {
  console.log(buttonId);
  var dots = document.getElementById(buttonId + "_dots");
  var moreText = document.getElementById(buttonId + "_more");
  var btnText = document.getElementById(buttonId);

  if (dots.style.display === "none") {
    dots.style.display = "inline";
    btnText.innerHTML = "Afficher plus";
    moreText.style.display = "none";
  } else {
    dots.style.display = "none";
    btnText.innerHTML = "Afficher Moins";
    moreText.style.display = "inline";
  }
}
