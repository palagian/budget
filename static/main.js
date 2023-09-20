const toggleDisplay = (element, displayValue) => {
    element.style.display = displayValue;
};

function updateTotals() {
    updateRowTotals();
    updateColumnTotals();
}

function updateRowTotals() {
    const totalRowCells = document.querySelectorAll(".total-row");
    totalRowCells.forEach(cell => {
        const parentRow = cell.parentNode;
        const planInputs = parentRow.querySelectorAll(".plan-input");
        let total = 0;
        planInputs.forEach(input => {
            const value = parseFloat(input.value);
            if (!isNaN(value)) {
                total += value;
            }
        });
        cell.textContent = total.toFixed(1);
    });
}

function updateColumnTotals() {
    const totalColumnCells = document.querySelectorAll(".total-column");
    totalColumnCells.forEach((cell, columnIndex) => {
        const planInputs = document.querySelectorAll(`.plan-input[data-month="${columnIndex - 2}"]`);
        let total = 0;
        planInputs.forEach(input => {
            const value = parseFloat(input.value);
            if (!isNaN(value)) {
                total += value;
            }
        });
        cell.textContent = total.toFixed(1);
    });

    const grandTotalCell = document.querySelector(".grand-total");
    let grandTotal = 0;
    totalColumnCells.forEach(cell => {
        const total = parseFloat(cell.textContent);
        if (!isNaN(total)) {
            grandTotal += total;
        }
    });
    grandTotalCell.textContent = grandTotal.toFixed(1);
}

const planInputs = document.querySelectorAll(".plan-input");
planInputs.forEach(input => {
    input.addEventListener("change", function () {
        updateTotals();
    });
});

const kamDropdowns = document.querySelectorAll(".kam-dropdown");
kamDropdowns.forEach(dropdown => {
    dropdown.addEventListener("change", function () {
        const selectedKAM = this.value;
        const rowNumber = this.getAttribute("data-row");
        const clientDropdown = document.querySelector(`.client-dropdown[data-row="${rowNumber}"]`);
        const clientInput = document.querySelector(`.client-input[data-row="${rowNumber}"]`);
        updateClientDropdownOptions(clientDropdown, clientInput, selectedKAM);
        updateTotals();
    });
});

const clientDropdowns = document.querySelectorAll(".client-dropdown");
clientDropdowns.forEach(dropdown => {
    const clientInput = dropdown.parentNode.querySelector(".client-input");
    // Dropdown change event
    dropdown.addEventListener("change", function () {
        const selectedValue = this.value;

        if (selectedValue === "0") {
            toggleDisplay(this, "none");
            toggleDisplay(clientInput, "inline");
            clientInput.value = "";
            clientInput.focus();
        } else {
            toggleDisplay(clientInput, "none");
            toggleDisplay(this, "inline");
            const projectDropdown = document.querySelector(".project-dropdown");
            const rowNumber = this.getAttribute("data-row");
            const selectedClient = selectedValue;
            console.log(`Selected Client ID: ${selectedClient}`);
            updateProjectDropdownOptions(projectDropdown, selectedClient);
        }
    });

    // Input blur event
    clientInput.addEventListener("blur", function () {
        if (this.value === "") {
            toggleDisplay(this, "none");
            toggleDisplay(dropdown, "inline");
            dropdown.selectedIndex = 0; // Reset dropdown to first option
        }
    });

    // Input keydown event to capture 'Enter' key
    clientInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            if (this.value === "") {
                toggleDisplay(this, "none");
                toggleDisplay(dropdown, "inline");
                dropdown.selectedIndex = 0;
            }
        }
    });
});


const projectDropdowns = document.querySelectorAll(".project-dropdown");
projectDropdowns.forEach(dropdown => {
    dropdown.addEventListener("change", function () {
        const selectedValue = this.value;
        const projectInput = this.parentNode.querySelector(".project-input");
        if (selectedValue === "0") {
            this.style.display = "none";
            projectInput.style.display = "inline";
            projectInput.value = "";
            projectInput.focus();
        } else {
            projectInput.style.display = "none";
            this.style.display = "inline";
        }
    });
});


function updateClientDropdownOptions(clientDropdown, clientInput, selectedKAM) {
    fetch(`/get_clients_for_kam/${selectedKAM}`)
        .then(response => response.json())
        .then(data => {
            clientDropdown.innerHTML = '<option value="" selected>Select Client</option>';
            data.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.id;
                optionElement.textContent = option.name;
                clientDropdown.appendChild(optionElement);
            });
            const otherClientOption = document.createElement('option');
            otherClientOption.value = '0';
            otherClientOption.textContent = 'Other Client';
            clientDropdown.appendChild(otherClientOption);
        })
        .catch(error => {
            console.error('Error fetching clients:', error);
        });
}

function updateProjectDropdownOptions(projectDropdown, selectedClient) {
    const url = `/get_projects_for_client/${selectedClient}`;
    console.log(`Request URL: ${url}`);

    if (projectDropdown) {
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Network response was not ok: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // console.log(data);
                projectDropdown.innerHTML = '<option value="" selected>Select Project</option>';
                data.forEach(option => {
                    const optionElement = document.createElement('option');
                    optionElement.value = option.id;
                    optionElement.textContent = option.name;
                    projectDropdown.appendChild(optionElement);

                    // console.log(optionElement.value);
                    // console.log(optionElement.textContent);
                });
                const otherProjectOption = document.createElement('option');
                otherProjectOption.value = '0';
                otherProjectOption.textContent = 'Other Project';
                projectDropdown.appendChild(otherProjectOption);
            })
            .catch(error => {
                console.error('Error fetching projects:', error);
            });
    } else {
        console.error("projectDropdown не ініціалізовано або має значення null.");
    }
}


// Call the updateTotals function when the page loads to initialize the totals
updateTotals();
