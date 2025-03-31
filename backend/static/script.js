document.addEventListener("DOMContentLoaded", () => {
    const targetList = document.getElementById("target-list");
    targetList.innerHTML = ""; // Clear the list

    // Fetch saved targets
    fetch("/api/targets")
        .then((response) => response.json())
        .then((data) => {
            data.forEach((target) => {
                const listItem = document.createElement("li");
                listItem.innerHTML = `
                    ${target.name} (${target.ip})
                    <button class="delete-btn" data-id="${target.id}">Delete</button>
                `;
                targetList.appendChild(listItem);

                // Add event listener to the delete button
                listItem.querySelector(".delete-btn").addEventListener("click", (event) => {
                    const targetId = event.target.getAttribute("data-id");
                    deleteTarget(targetId, listItem);
                });
            });
        })
        .catch((error) => {
            console.error("Error fetching targets:", error);
        });
});

document.getElementById("target-form").addEventListener("submit", (event) => {
    event.preventDefault();

    const targetName = document.getElementById("target-name").value;
    const targetIP = document.getElementById("target-ip").value;

    // Send the target data to the backend
    fetch("/api/targets", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: targetName, ip: targetIP }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);

                // Add the target to the list
                const listItem = document.createElement("li");
                listItem.innerHTML = `
                    ${targetName} (${targetIP})
                    <button class="delete-btn" data-id="${data.id}">Delete</button>
                `;
                document.getElementById("target-list").appendChild(listItem);

                // Add event listener to the delete button
                listItem.querySelector(".delete-btn").addEventListener("click", (event) => {
                    const targetId = event.target.getAttribute("data-id");
                    deleteTarget(targetId, listItem);
                });
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("Failed to add target.");
        });

    // Clear the form
    event.target.reset();
});

// Function to send target server to the API
function sendTargetToAPI(target) {
    fetch('http://127.0.0.1:8080/api/targets', {
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
    const targetForm = document.getElementById("target-form");
    const targetList = document.getElementById("target-list");

    targetForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const targetName = document.getElementById("target-name").value;
        const targetIP = document.getElementById("target-ip").value;

        // Send the target data to the backend
        fetch("/api/targets", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name: targetName, ip: targetIP }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    alert(data.error);
                } else {
                    alert(data.message);

                    // Add the target to the list
                    const listItem = document.createElement("li");
                    listItem.textContent = `${targetName} (${targetIP})`;
                    targetList.appendChild(listItem);
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Failed to add target.");
            });

        // Clear the form
        targetForm.reset();
    });
});

document.getElementById("target-form").addEventListener("submit", (event) => {
    event.preventDefault();

    const targetName = document.getElementById("target-name").value;
    const targetIP = document.getElementById("target-ip").value;

    // Send the target data to the backend
    fetch("/api/targets", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: targetName, ip: targetIP }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);

                // Add the target to the list
                const listItem = document.createElement("li");
                listItem.innerHTML = `
                    ${targetName} (${targetIP})
                    <button class="delete-btn" data-id="${data.id}">Delete</button>
                `;
                document.getElementById("target-list").appendChild(listItem);

                // Add event listener to the delete button
                listItem.querySelector(".delete-btn").addEventListener("click", (event) => {
                    const targetId = event.target.getAttribute("data-id");
                    deleteTarget(targetId, listItem);
                });
            }
            if (!targetName || !targetIP) {
                console.error("Target name or IP is empty!");
                return;
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("Failed to add target.");
        });

    // Clear the form
    event.target.reset();
});

// Function to delete a target
function deleteTarget(targetId, listItem) {
    fetch(`/api/targets/${targetId}`, {
        method: "DELETE",
    })
        .then((response) => response.json())
        .then((data) => {
            alert(data.message);
            listItem.remove(); // Remove the target from the list
        })
        .catch((error) => {
            console.error("Error deleting target:", error);
            alert("Failed to delete target.");
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
                // Display the command output in the terminal view
                const output = document.createElement("pre");
                output.textContent = data.output;
                terminalOutput.appendChild(output);

                // Scroll to the bottom of the terminal output
                terminalOutput.scrollTop = terminalOutput.scrollHeight;
            })
            .catch((error) => {
                console.error("Error executing command:", error);
                const errorOutput = document.createElement("pre");
                errorOutput.textContent = "Error executing command.";
                terminalOutput.appendChild(errorOutput);
            });

        // Clear the command input
        terminalForm.reset();
    });
});

document.getElementById("target-form").addEventListener("submit", (event) => {
    event.preventDefault();

    const targetName = document.getElementById("target-name").value;
    const targetIP = document.getElementById("target-ip").value;

    // Send the target data to the backend
    fetch("/api/targets", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: targetName, ip: targetIP }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(data.message);

                // Add the target to the list
                const listItem = document.createElement("li");
                listItem.innerHTML = `
                    ${targetName} (${targetIP})
                    <button class="delete-btn" data-id="${data.id}">Delete</button>
                `;
                document.getElementById("target-list").appendChild(listItem);

                // Add event listener to the delete button
                listItem.querySelector(".delete-btn").addEventListener("click", (event) => {
                    const targetId = event.target.getAttribute("data-id");
                    deleteTarget(targetId, listItem);
                });
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("Failed to add target.");
        });

    // Clear the form
    event.target.reset();
});