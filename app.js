// app.js

const serverList = document.getElementById("server-list");
const createBtn = document.getElementById("create-server-btn");
const serverNameInput = document.getElementById("server-name");
const ownerInput = document.getElementById("owner-name");

// Load all servers from backend
async function loadServers() {
    const res = await fetch("/servers");
    if (!res.ok) return console.error("Failed to load servers");
    const servers = await res.json();

    serverList.innerHTML = "";
    servers.forEach(s => {
        const div = document.createElement("div");
        div.className = "server-item";
        div.textContent = `${s.id}: ${s.name} (Owner: ${s.owner})`;
        div.addEventListener("click", () => {
            // Save server ID to localStorage for server.html
            localStorage.setItem("currentServerId", s.id);
            window.location.href = "server.html";
        });
        serverList.appendChild(div);
    });
}

// Create a new server
createBtn.addEventListener("click", async () => {
    const name = serverNameInput.value.trim();
    const owner = ownerInput.value.trim();
    if (!name || !owner) return alert("Fill both fields!");

    const res = await fetch("/servers/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, owner })
    });

    if (res.ok) {
        serverNameInput.value = "";
        ownerInput.value = "";
        loadServers();
    } else {
        alert("Failed to create server");
    }
});

// Initial load
loadServers();
