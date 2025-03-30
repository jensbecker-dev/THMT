document.addEventListener("DOMContentLoaded", () => {
    const dropdownBtn = document.querySelector(".dropdown-btn");
    const dropdownMenu = document.querySelector(".dropdown-menu");

    // Toggle dropdown menu visibility on click
    dropdownBtn.addEventListener("click", (event) => {
        event.preventDefault(); // Prevent default link behavior
        dropdownMenu.classList.toggle("show");
    });

    // Close dropdown menu if clicked outside
    document.addEventListener("click", (event) => {
        if (!dropdownBtn.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.remove("show");
        }
    });
});