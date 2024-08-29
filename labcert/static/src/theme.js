"use strict";

(function () {
    let themeToggle = document.getElementById("themeToggle")

    if (themeToggle) {
        if (localStorage.getItem("color-theme") === "dark" || (!("color-theme" in localStorage) && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
            themeToggle.checked = true
        } else {
            themeToggle.checked = false
        }

        themeToggle.addEventListener("click", function () {
            if (themeToggle.checked) {
                localStorage.setItem("color-theme", "dark")
                document.documentElement.classList.add("dark")
            } else {
                localStorage.setItem("color-theme", "light")
                document.documentElement.classList.remove("dark")
            }
        })
    }

})()