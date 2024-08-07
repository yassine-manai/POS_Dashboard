function openEditModal(carparkId, name, ip, username, password) {
    document.getElementById('editForm').action = `/edit/${carparkId}/${name}`;
    document.getElementById('editCarparkId').value = carparkId;
    document.getElementById('editPosName').value = name;
    document.getElementById('name').value = name;
    document.getElementById('ip').value = ip;
    document.getElementById('username').value = username;
    document.getElementById('password').value = password;

    document.getElementById('editModal').style.display = 'flex';
}

function openAddModal(carparkId, carparkName) {
    document.getElementById('addForm').action = `/add/${carparkId}`;
    document.getElementById('addCarparkId').value = carparkId;
    document.getElementById('site').value = carparkName; // Set the site to carpark name
    document.getElementById('addModal').style.display = 'flex';

    // Remove previous event listeners
    const form = document.getElementById('addForm');
    const newForm = form.cloneNode(true);
    form.parentNode.replaceChild(newForm, form);

    // Add new event listener
    newForm.addEventListener('submit', function(event) {
        event.preventDefault();
        checkPosExistence(carparkId);
    });
}

// ... rest of the JavaScript remains the same

function openAddModal() {
    document.getElementById('addModal').style.display = 'flex';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}


