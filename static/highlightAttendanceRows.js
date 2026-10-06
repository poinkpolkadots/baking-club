function highlightAttendanceRows() {
    const broughtCells = document.querySelectorAll(".baked-goods-brought");
    for (const cell of broughtCells) {
        if (cell.innerText === "0") {
            cell.style.backgroundColor = "red"; // later change to using variables
        }
    }

    const latestMeetingCells = document.querySelectorAll(".latest-meeting");
    const present = new Date()
    for (const cell of latestMeetingCells) {
        const cellDate = new Date(cell.innerText);
        if ((Math.abs(present.getMonth() - cellDate.getMonth() > 3)) || cell.innerText === "Nothing has been brought!") {
            cell.style.backgroundColor = "red"; // later change to using variables
        }
    }
}

document.addEventListener("DOMContentLoaded", highlightAttendanceRows);