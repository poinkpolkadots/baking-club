function highlightStatus() {
    const statusElements = document.getElementsByClassName("status");
    const statusMarker = document.getElementById("status");

    if (statusElements[0].innerText.charAt(statusElements[0].innerText.length - 1) === "0") {
        statusMarker.innerText = "Not in good standing";
    }

    if (statusElements[1].innerText.charAt(statusElements[0].innerText.length - 1) === "0") {
        statusMarker.innerText = "Not in good standing";
    }

    if (statusElements[2].innerText.includes("Nothing has been brought!")) {
        statusMarker.innerText = "Not in good standing";
    }
}

document.addEventListener("DOMContentLoaded", highlightStatus);