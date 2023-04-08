let isThemeInLocalStorage = "color-theme" in localStorage
let isBrowserInDarkMode = window.matchMedia("(prefers-color-scheme: dark)").matches
let isThemeSetToDarkMode = localStorage.getItem("color-theme") === "dark"

var pageSize = 10
let isPageSizeInLocalStorage = "page-size" in localStorage

// Set dark theme accordingly
if (isThemeSetToDarkMode || (!isThemeInLocalStorage && isBrowserInDarkMode)) {
    document.documentElement.classList.add("dark")
} else {
    document.documentElement.classList.remove("dark")
}

// Set default page size if not defined
if (isPageSizeInLocalStorage) {
    pageSize = parseInt(localStorage.getItem("page-size"))
} else {
    localStorage.setItem("page-size", pageSize)
}