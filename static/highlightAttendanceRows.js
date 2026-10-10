function highlightAttendanceRows() {
    const broughtCells = document.getElementsByClassName("baked-goods-brought");
    for (const cell of broughtCells) {
        if (cell.innerText === "0") {
            cell.style.backgroundColor = "var(--accent4)"; // later change to using variables
        }
    }

    const latestMeetingCells = document.getElementsByClassName("latest-meeting");
    for (const cell of latestMeetingCells) {
        if (cell.innerText === "Nothing has been brought!") {
            cell.style.backgroundColor = "var(--accent4)"; // later change to using variables
        }
    }

    const meetingsAttended = document.getElementsByClassName("meetings-attended");
    for (const cell of meetingsAttended) {
        if (cell.innerText ==="0") {
            cell.style.backgroundColor = "var(--accent4)";
        }
    }
}

document.addEventListener("DOMContentLoaded", highlightAttendanceRows);