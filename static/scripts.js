function showBakedGoodInput() {
    var broughtBakedGoodInput = document.getElementsByName("brought-baked-good");
    var bakedGoodInput = document.getElementsByClassName("baked-good");
    if (broughtBakedGoodInput.value === "true") {
        bakedGoodInput.style.visibility = "visible";
    } else {
        bakedGoodInput.style.visibility = "hidden";
    }
}