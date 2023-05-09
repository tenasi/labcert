"use strict"

var pageSize = 10

var rsaDefaultStrength = 4096;

(function () {
    let isThemeInLocalStorage = "color-theme" in localStorage
    let isBrowserInDarkMode = window.matchMedia("(prefers-color-scheme: dark)").matches
    let isThemeSetToDarkMode = localStorage.getItem("color-theme") === "dark"

    // Set dark theme accordingly
    if (isThemeSetToDarkMode || (!isThemeInLocalStorage && isBrowserInDarkMode)) {
        document.documentElement.classList.add("dark")
    } else {
        document.documentElement.classList.remove("dark")
    }

    // Set default page size if not defined
    if ("page-size" in localStorage) {
        pageSize = parseInt(localStorage.getItem("page-size"))
    } else {
        localStorage.setItem("page-size", pageSize)
    }

    if ("rsa-default-strength" in localStorage) {
        rsaDefaultStrength = parseInt(localStorage.getItem("rsa-default-strength"))
    } else {
        localStorage.setItem("rsa-default-strength", rsaDefaultStrength)
    }
})()
