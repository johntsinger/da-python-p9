document.addEventListener("DOMContentLoaded", function(event) {
    document.getElementById("id_image").onchange = function () {
        var src = URL.createObjectURL(this.files[0])
        document.getElementById("image").src = src
        document.getElementById("selected-image").classList.remove("d-none")
    }
})
