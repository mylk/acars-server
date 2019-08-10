window.onload = function () {
    var buttons = document.querySelectorAll(".txt-title");

    for (var i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener("click", function() {
            var container = this.parentElement.querySelector(".txt-msg");
            if (container.classList.contains("fadeout")) {
                container.classList.remove("fadeout");
                container.classList.add("fadein");
            } else {
                container.classList.remove("fadein");
                container.classList.add("fadeout");
            }
        });
    }
};
