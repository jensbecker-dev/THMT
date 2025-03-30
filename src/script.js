document.addEventListener("DOMContentLoaded", () => {
    const targetForm = document.getElementById("target-form");
    const targetList = document.getElementById("target-list");
    const listTargetsBtn = document.getElementById("list-targets-btn");
    const targetModal = document.getElementById("target-modal");
    const allTargetsList = document.getElementById("all-targets-list");
    const closeModalBtn = document.querySelector(".close-btn");

    // Array to store targets
    const targets = [];

    // Handle form submission
    targetForm.addEventListener("submit", (event) => {
        event.preventDefault();

        // Get input values
        const targetName = document.getElementById("target-name").value;
        const targetIP = document.getElementById("target-ip").value;

        // Add target to the array
        targets.push({ name: targetName, ip: targetIP });

        // Create a new list item
        const listItem = document.createElement("li");
        listItem.innerHTML = `
            <span>${targetName} (${targetIP})</span>
            <button class="delete-btn">Delete</button>
        `;

        // Add delete functionality
        listItem.querySelector(".delete-btn").addEventListener("click", () => {
            targetList.removeChild(listItem);
            // Remove target from the array
            const index = targets.findIndex(
                (target) => target.name === targetName && target.ip === targetIP
            );
            if (index !== -1) targets.splice(index, 1);
        });

        // Append the new item to the list
        targetList.appendChild(listItem);

        // Clear the form inputs
        targetForm.reset();
    });

    // Handle "List All Targets" button click
    listTargetsBtn.addEventListener("click", () => {
        // Clear the modal list
        allTargetsList.innerHTML = "";

        // Populate the modal list with all targets
        targets.forEach((target) => {
            const listItem = document.createElement("li");
            listItem.textContent = `${target.name} (${target.ip})`;
            allTargetsList.appendChild(listItem);
        });

        // Show the modal
        targetModal.style.display = "block";
    });

    // Handle modal close button click
    closeModalBtn.addEventListener("click", () => {
        targetModal.style.display = "none";
    });

    // Close modal when clicking outside the modal content
    window.addEventListener("click", (event) => {
        if (event.target === targetModal) {
            targetModal.style.display = "none";
        }
    });
});