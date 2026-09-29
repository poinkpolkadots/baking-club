const radios = document.querySelectorAll('input[name="brought-baked-good"]');
const section = document.getElementById("baked-good-section");
const input = document.getElementById("baked-good");

console.log(radios)

function showBakedGoodInput() {
    function updateBakedGoodVisibility() {
        const selected = document.querySelector('input[name="brought-baked-good"]:checked');
        const show = selected !== null && selected.value === "true";

        section.hidden = !show;
        input.disabled = !show;
        input.required = show;
        if (!show) input.value = "";
    }

    radios.forEach(radio => radio.addEventListener("change", updateBakedGoodVisibility));
    updateBakedGoodVisibility(); // set correct initial state
}

document.addEventListener("DOMContentLoaded", showBakedGoodInput);