document.addEventListener("DOMContentLoaded", () => {
    const targetForm = document.getElementById("target-form");
    const targetList = document.getElementById("target-list");
    const listTargetsBtn = document.getElementById("list-targets-btn");
    const targetModal = document.getElementById("target-modal");
    const allTargetsList = document.getElementById("all-targets-list");
    const closeModalBtn = document.querySelector(".close-btn");

    // Array to store targets
    const targets = [];
    
targetForm.addEventListener("submit", (event) => {
    event.preventDefault();

    // Get input values
    const targetName = document.getElementById("target-name").value;
    const targetIP = document.getElementById("target-ip").value;

    // Create target object
    const target = { name: targetName, ip: targetIP };

    // Add target to the array
    targets.push(target);

    // Send target to the API
    sendTargetToAPI(target);

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
            (t) => t.name === targetName && t.ip === targetIP
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

// Function to send target server to the API
function sendTargetToAPI(target) {
    fetch('http://127.0.0.1:5000/api/targets', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(target),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            console.log('Target successfully sent to API:', data);
            alert(data.message); // Display success message
        })
        .catch((error) => {
            console.error('Error sending target to API:', error);
            alert('Failed to send target to API. Please try again.');
        });
}
document.addEventListener("DOMContentLoaded", () => {
    const terminalForm = document.getElementById("terminal-form");
    const terminalOutput = document.getElementById("terminal-output");

    terminalForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const commandInput = document.getElementById("command-input").value;

        // Send the command to the backend
        fetch("/execute-command", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `command=${encodeURIComponent(commandInput)}`,
        })
            .then((response) => response.json())
            .then((data) => {
                // Display the command output
                terminalOutput.textContent = data.output;
            })
            .catch((error) => {
                console.error("Error executing command:", error);
                terminalOutput.textContent = "Error executing command.";
            });
    });
});