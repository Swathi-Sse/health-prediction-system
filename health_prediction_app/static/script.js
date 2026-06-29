const searchInput = document.getElementById("searchInput");

if (searchInput) {
    searchInput.addEventListener("keyup", function () {
        const value = this.value.toLowerCase();
        const rows = document.querySelectorAll("#patientTable tbody tr");

        rows.forEach(function (row) {
            row.style.display = row.innerText.toLowerCase().includes(value) ? "" : "none";
        });
    });
}
