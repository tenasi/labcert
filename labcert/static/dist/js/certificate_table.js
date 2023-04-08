// Load certificaates table and rows
const certificateTable = document.getElementById("certificateTable")
const certificates = certificateTable.tBodies[0].rows

// Load filter checkboxes
const filterRootCheckbox = document.getElementById("filterRootCheckbox")
const filterInterCheckbox = document.getElementById("filterInterCheckbox")
const filterEndCheckbox = document.getElementById("filterEndCheckbox")
const filterValidCheckbox = document.getElementById("filterValidCheckbox")
const filterExpiredCheckbox = document.getElementById("filterExpiredCheckbox")
const filterRevokedCheckbox = document.getElementById("filterRevokedCheckbox")
const filterErrorCheckbox = document.getElementById("filterErrorCheckbox")
// Load search bar input
const searchInput = document.getElementById("searchInput")

// Load page bar and buttons
const pageButtonList = document.getElementById("pageButtonList")
const pageButtons = Array.from(pageButtonList.children).slice(1, 6)
const previousPageButton = document.getElementById("previousPageButton")
const page1Button = document.getElementById("page1Button")
const page2Button = document.getElementById("page2Button")
const page3Button = document.getElementById("page3Button")
const page4Button = document.getElementById("page4Button")
const page5Button = document.getElementById("page5Button")
const nextPageButton = document.getElementById("nextPageButton")
const displayedNumberOfCerts = document.getElementById("displayedNumberOfCerts")
const totalNumberOfCerts = document.getElementById("totalNumberOfCerts")
// Define selected page button classes
const currentPageButtonClasses = [
    "text-primary-600",
    "bg-primary-50",
    "border",
    "border-primary-300",
    "hover:bg-primary-100",
    "hover:text-primary-700",
    "dark:border-gray-700",
    "dark:bg-gray-700",
    "dark:text-white"
]
// Define unselected page button classes
const normalPageButtonClasses = [
    "text-gray-500",
    "bg-white",
    "border",
    "border-gray-300",
    "hover:bg-gray-100",
    "hover:text-gray-700",
    "dark:bg-gray-800",
    "dark:border-gray-700",
    "dark:text-gray-400",
    "dark:hover:bg-gray-700",
    "dark:hover:text-white"
]

// This variable controls the page currently displayed in the view
var currentPage = 1
// This variable contains a whitelist of all active filters
var filter = new Set()
// This variable defines the function used to match the search query
var match = function (_, _) { return true }
// This variable controls if a table row is visible or not
var matches = {}
for (let i = 0; i < certificates.length; i++) {
    // Match all per default
    matches[i] = true
}
// This variable stores the total number of matches with given filters applied
var numberOfMatches = certificates.length
// This variable stores the total number of pages with given filters applied
var numberOfPages = Math.ceil(numberOfMatches / pageSize)

// This variable holds the level of the last shown row
var indentLevel = 0
// This variable holds the indent factor of the last shown row
var indentFactor = 0

/**
 * Updates the browser view based on the selection in the variable @var matches
 */
function updateView() {
    // This variable counts the rows shown on the current page
    let counter = 0

    // Iterate through all rows to hide or unhide the rows based on the filter and current page number
    for (let i = 0; i < certificates.length; i++) {
        // Check if filter applies
        if (matches[i]) {
            // If filter applies increase counter and check if item is to be shown on the current page
            counter++
            if ((currentPage - 1) * pageSize < counter && counter <= currentPage * pageSize) {
                // If item is on current page, show item in table
                certificates[i].classList.remove("hidden")
                // Parse current indent from classList
                let oldIndent = certificates[i].cells[0].classList[0]
                // Check if level is increasing
                let newLevel = parseInt(certificates[i].cells[1].innerText.trim())
                if (newLevel > indentLevel) {
                    // If level is increasing, remember new level and increase indent factor
                    indentLevel = newLevel
                    indentFactor++
                } else if (newLevel < indentLevel) {
                    // If level is decreasing, remember new level and decrease indent factor accordingly
                    let diff = indentLevel - newLevel
                    indentLevel = newLevel
                    indentFactor = indentFactor - diff
                }
                // Calculate indent and create corresponding indent class tring
                let newIndent = `pl-${Math.min(indentFactor * 4, 64)}`
                // Replace old indent with new indent
                certificates[i].cells[0].classList.replace(oldIndent, newIndent)
            } else {
                // If item is not on current page, hide item in table
                certificates[i].classList.add("hidden")
            }
        } else {
            // If item does not match filter, hide item in table
            certificates[i].classList.add("hidden")
        }
    }
    // Update page bar
    updatePages()
}

/**
 * Update page bar based on @var numberOfPages and @var currentPage
 */
function updatePages() {
    // Construct and set page item range indicator
    firstEntryNumber = (currentPage - 1) * pageSize + 1
    lastEntryNumber = Math.min((currentPage) * pageSize, numberOfMatches)
    displayedNumberOfCerts.textContent = `${firstEntryNumber} - ${lastEntryNumber}`
    totalNumberOfCerts.textContent = numberOfMatches
    // Iterate through each page button and set default values
    for (let i = 0; i < 5; i++) {
        // Unhide page button
        pageButtons[i].classList.remove("hidden")
        // Set unselected page button style
        pageButtons[i].children[0].classList.remove(...currentPageButtonClasses)
        pageButtons[i].children[0].classList.add(...normalPageButtonClasses)
        // Set page button numbering from 1 to 5
        pageButtons[i].children[0].textContent = i + 1
    }
    // Iterate through each page button that is not active
    for (let i = numberOfPages; i < 5; i++) {
        // Hide page button
        pageButtons[i].classList.add("hidden")
    }
    // Check if number of pages exceed the number of page buttons
    if (numberOfPages > 5) {
        // Define index to access page button for current page
        let index = currentPage - 1
        // Define reverse index to acces spage button from other direction
        let indexReverse = 4 - (numberOfPages - currentPage)
        // Check what page button layout must be used
        if (currentPage <= 3) {
            // Define page button layout when current page is within first three pages: 1  2  3 ... 10
            pageButtons[1].children[0].textContent = 2
            pageButtons[2].children[0].textContent = 3
            pageButtons[3].children[0].textContent = "..."
            pageButtons[4].children[0].textContent = numberOfPages
            // Update view to show active page
            pageButtons[index].children[0].classList.remove(...normalPageButtonClasses)
            pageButtons[index].children[0].classList.add(...currentPageButtonClasses)
        } else if (indexReverse <= 1) {
            // Define page button layout when current page is between first and last three pages: 1 ... 6 ... 10
            pageButtons[1].children[0].textContent = "..."
            pageButtons[2].children[0].textContent = currentPage
            pageButtons[3].children[0].textContent = "..."
            pageButtons[4].children[0].textContent = numberOfPages
            // Update view to show active page
            pageButtons[2].children[0].classList.remove(...normalPageButtonClasses)
            pageButtons[2].children[0].classList.add(...currentPageButtonClasses)
        } else {
            // Define page button layout when current page is within last three pages: 1 ... 8  9  10
            pageButtons[1].children[0].textContent = "..."
            pageButtons[2].children[0].textContent = numberOfPages - 2
            pageButtons[3].children[0].textContent = numberOfPages - 1
            pageButtons[4].children[0].textContent = numberOfPages
            // Update view to show active page
            pageButtons[indexReverse].children[0].classList.remove(...normalPageButtonClasses)
            pageButtons[indexReverse].children[0].classList.add(...currentPageButtonClasses)
        }
    } else {
        // Define index to access page button for current page
        let index = currentPage - 1
        // Update view to show active page
        pageButtons[index].children[0].classList.remove(...normalPageButtonClasses)
        pageButtons[index].children[0].classList.add(...currentPageButtonClasses)
    }
}

/**
 * Update matches based on selected @var filter and @var match function
 */
function updateMatches() {
    // Iterate through all items
    for (let i = 0; i < certificates.length; i++) {
        // Get row from table
        let row = certificates[i]
        // Get certificate name from row
        let certName = row.cells[0].innerText.trim().toLowerCase()
        // Get certificate issuer id from row
        let certIssuerId = row.cells[2].innerText.trim()
        // Get certificate issuer name from row
        let certIssuer = row.cells[3].innerText.trim().toLowerCase()
        // Get certificate catgory from row
        let certCategory = row.cells[4].innerText.trim()
        // Get certificate status from row
        let certStatus = row.cells[7].innerText.trim()
        // Check if certificate matches filter and match function
        if (filter.has(certCategory) && filter.has(certStatus) && match(certName, certIssuer)) {
            // If certificate matches set corresponding entry in matches
            matches[i] = true
            // Ensure that all issuing certificates in the chain are also included in matches
            while (certIssuerId) {
                certIssuerId = parseInt(certIssuerId) - 1
                matches[certIssuerId] = filter.has(certificates[certIssuerId].cells[4].innerText.trim())
                certIssuerId = certificates[certIssuerId].cells[2].innerText.trim()
            }
        } else {
            // If certificate does not match, remove it from matches
            matches[i] = false
        }
    }
    // Calculate total number of matches
    numberOfMatches = 0
    for (let m in matches) {
        numberOfMatches += matches[m]
    }
    // Calculate number of pages needed to display all matchese
    numberOfPages = Math.ceil(numberOfMatches / pageSize)
    // Reset current page to first page
    currentPage = 1
    // Reset indent level
    indentLevel = 0
    // Reset indent factor
    indentFactor = 0
    // Update browser view
    updateView()
}

/**
 * Update @var filter by querying checkboxes
 */
function updateFilter() {
    // Create empty filter set
    filter = new Set()
    // Check if Root CA checkbox is set and add to filter if set
    if (filterRootCheckbox.checked) {
        filter.add("Root CA")
    }
    // Check if Intermediate checkbox is set and add to filter if set
    if (filterInterCheckbox.checked) {
        filter.add("Intermediate")
    }
    // Check if End Entity checkbox is set and add to filter if set
    if (filterEndCheckbox.checked) {
        filter.add("End Entity")
    }
    // Check if Valid checkbox is set and add to filter if set
    if (filterValidCheckbox.checked) {
        filter.add("Valid")
    }
    // Check if Expired checkbox is set and add to filter if set
    if (filterExpiredCheckbox.checked) {
        filter.add("Expired")
    }
    // Check if Revoked checkbox is set and add to filter if set
    if (filterRevokedCheckbox.checked) {
        filter.add("Revoked")
    }
    // Check if Error checkbox is set and add to filter if set
    if (filterErrorCheckbox.checked) {
        filter.add("Error")
    }
    // Update matches to reflect filter changes
    updateMatches()
}

/**
 * Update @var match function by querying search input
 */
function updateSearch() {
    // Query search string
    let search = searchInput.value.trim()
    // Check if search string includes issuer or regex flag
    if (search.includes("issuer:") && !search.endsWith("issuer:")) {
        // If search string includes issuer flag, parse it
        let index = search.indexOf("issuer:")
        let searchIssuer = search.substring(index + 7).toLowerCase()
        let searchString = search.substring(0, index).toLowerCase().trim()
        // Define match function accordingly
        match = function (certName, certIssuer) {
            return certName.includes(searchString) && certIssuer.includes(searchIssuer)
        }
    } else if (search.length > 6 && search.startsWith("regex:")) {
        // If search string includes regex flag, parse it
        let searchRegex = search.substring(6)
        // Define match function accordingly
        match = function (certName, _) {
            return certName.match(searchRegex)
        }
    } else if (search.length > 0) {
        // If search string is not empty, define match function accordingly
        match = function (certName, _) {
            return certName.includes(search.toLowerCase())
        }
    } else {
        // If search string is empty, define match function accordingly
        match = function (_, _) { return true }
    }
    // Update matches to reflect match function change
    updateMatches()
}

// Event listener function for next page button
function nextPage() {
    // Set current page to next page if possible
    currentPage = Math.min(currentPage + 1, numberOfPages)
    // Update view to reflect new page
    updateView()
}

// Event listener function for previous page button
function previousPage() {
    // Set current page to previous page if possible
    currentPage = Math.max(currentPage - 1, 1)
    // Update view to reflect new page
    updateView()
}

// Event listener function for first page button
function page1() {
    // Set current page to first page
    currentPage = 1
    // Update view to reflect new page
    updateView()
}

// Event listener function for second page button
function page2() {
    // Check if second page button is clickable
    if (numberOfPages <= 5 || currentPage <= 3) {
        // Set current page to second page
        currentPage = 2
        // Update view to reflect new page
        updateView()
    }
}

// Event listener function for third page button
function page3() {
    // Check if third page button is clickable and should direct to third or third last page
    if (numberOfPages <= 5 || currentPage <= 3) {
        // Set current page to third page
        currentPage = 3
        // Update view to reflect new page
        updateView()
    } else if (currentPage > numberOfPages - 2) {
        // Set current page to third last page
        currentPage = numberOfPages - 2
        // Update view to reflect new page
        updateView()
    }
}

// Event listener function for fourth page button
function page4() {
    // Check if fourth page is clickable and should direct to fourth or second last page
    if (numberOfPages <= 5) {
        // Set current page to fourth page
        currentPage = 4
        // Update view to reflect new page
        updateView()
    } else if (currentPage >= numberOfPages - 2) {
        // Set current page to second last page
        currentPage = numberOfPages - 1
        // Update view to reflect new page
        updateView()
    }
}

// Event listener function for fifth page button
function page5() {
    // Set current page to last page
    currentPage = numberOfPages
    // Update view to reflect new page
    updateView()
}

// Add event listener for filter checkboxes
filterRootCheckbox.addEventListener("click", updateFilter)
filterInterCheckbox.addEventListener("click", updateFilter)
filterEndCheckbox.addEventListener("click", updateFilter)
filterValidCheckbox.addEventListener("click", updateFilter)
filterExpiredCheckbox.addEventListener("click", updateFilter)
filterRevokedCheckbox.addEventListener("click", updateFilter)
filterErrorCheckbox.addEventListener("click", updateFilter)

// Add event listener for search input
searchInput.addEventListener("input", updateSearch)

// Add event listener for page bar buttons
nextPageButton.addEventListener("click", nextPage)
previousPageButton.addEventListener("click", previousPage)
page1Button.addEventListener("click", page1)
page2Button.addEventListener("click", page2)
page3Button.addEventListener("click", page3)
page4Button.addEventListener("click", page4)
page5Button.addEventListener("click", page5)

// Update filter and view based on current selection for the first time
updateFilter()