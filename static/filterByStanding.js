var filtered = false;
const broughtCells = document.getElementsByClassName("baked-goods-brought");
const latestMeetingCells = document.getElementsByClassName("latest-meeting");
const meetingsAttended = document.getElementsByClassName("meetings-attended");
const table = document.getElementById("table");
const rows = table.rows;

function filterByStanding() {
    if (filtered == true) {
        filtered = false;
        document.getElementById("filter").innerText = "Filter by Member Standing";
        for (i = 0; i < rows.length; i++) {
            rows[i].style.visibility = "visible";
        }
    } else {
        filtered = true;
        document.getElementById("filter").innerText = "Reset";

        for (i = 0; i < latestMeetingCells.length; i++) {
            const cellDate = new Date(latestMeetingCells[i].innerText).getMonth();
            if (!(broughtCells[i].innerText === "0" || broughtCells[i].innerText === "Nothing has been brought!" || meetingsAttended[i].innerText === "0")) {
                rows[i + 1].style.visibility = "hidden";
            }
        }
    }
}

document.getElementById("filter").addEventListener("click", filterByStanding);