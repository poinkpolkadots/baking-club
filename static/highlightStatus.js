function highlightStatus() {
    const statusElements = document.getElementsByClassName("status");
    const statusMarker = document.getElementById("status");
    if (statusElements[0].innerText.charAt(statusElements[0].innerText.length - 1) === "0") {
        statusMarker.innerText = "Not in good standing";
    }

    const present = new Date().getMonth();
    const latestBrought = new Date(statusElements[1].innerText).getMonth();
    if ((Math.abs(present - latestBrought) > 3) || statusElements[1].innerText === "Nothing has been brought!") {
        statusMarker.innerText = "Not in good standing";
    }
}

document.addEventListener("DOMContentLoaded", highlightStatus);