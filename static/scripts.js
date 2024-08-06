function openEditModal(hostName, hostname, ip, password) {
    document.getElementById('editForm').action = `/edit/${hostName}`;
    document.getElementById('host_name').value = hostName;
    document.getElementById('hostname').value = hostname;
    document.getElementById('ip').value = ip;
    document.getElementById('password').value = password;

    document.getElementById('editModal').style.display = 'flex';
}

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
