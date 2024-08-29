"use strict";

(function () {
    // Load creation form elements
    let certTypeRoot = document.getElementById("typeRootRadio")
    let certTypeIntermediate = document.getElementById("typeIntermediateRadio")
    let certTypeEnd = document.getElementById("typeEndEntityRadio")
    let selectIssuerTitle = document.getElementById("selectIssuerTitle")
    let selectIssuerContent = document.getElementById("selectIssuerContent")
    let certTypeInput = document.getElementById("cert_type")
    let certLevelInput = document.getElementById("cert_level")
    let issuerInput = document.getElementById("issuer_id")
    let subjectStrengthInput = document.getElementById("subject_strength")

    // Hide select issuer section from form
    function hideIssuingSelector() {
        if (!selectIssuerTitle.classList.contains("hidden")) {
            selectIssuerTitle.classList.add("hidden")
        }
        if (!selectIssuerContent.classList.contains("hidden")) {
            selectIssuerContent.classList.add("hidden")
        }
    }

    // Unhide select issuer section from form
    function unhideIssuingSelector() {
        selectIssuerTitle.classList.remove("hidden")
        selectIssuerContent.classList.remove("hidden")
    }

    // Set certificate type to Root CA in form
    function setTypeRoot() {
        certTypeInput.value = "Root CA"
        certLevelInput.value = 1
        hideIssuingSelector()
    }

    // Set certificate type to Intermediate in form
    function setTypeIntermediate() {
        certTypeInput.value = "Intermediate"
        unhideIssuingSelector()
        updateCertLevel()
    }

    // Set certificate type to End Entity in form
    function setTypeEnd() {
        certTypeInput.value = "End Entity"
        unhideIssuingSelector()
        updateCertLevel()
    }

    // Update certificate level according based on issuer selection
    function updateCertLevel() {
        if (issuerInput.value) {
            certLevelInput.value = parseInt(issuerInput.value.split(",")[1]) + 1
        } else {
            certLevelInput.value = ""
        }
    }

    // Set subjectStrength to default value
    subjectStrengthInput.value = rsaDefaultStrength

    // Add event listeners for form fields
    certTypeRoot.addEventListener("click", setTypeRoot)
    certTypeIntermediate.addEventListener("click", setTypeIntermediate)
    certTypeEnd.addEventListener("click", setTypeEnd)
    issuerInput.addEventListener("input", updateCertLevel)
})()