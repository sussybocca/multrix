async function fetchServers() {
    const res = await fetch('http://127.0.0.1:8000/servers');
    const servers = await res.json();
    const listDiv = document.getElementById("server-list");
    listDiv.innerHTML = "";
    servers.forEach(s => {
        const btn = document.createElement("button");
        btn.textContent = `${s.name} (Owner: ${s.owner})`;
        btn.onclick = () => window.open(`server.html?id=${s.id}&name=${s.name}`, "_blank");
        listDiv.appendChild(btn);
    });
}

async function createServer() {
    const name = prompt("Enter server name:");
    const owner = prompt("Enter your name:");
    if(!name || !owner) return;
    const res = await fetch('http://127.0.0.1:8000/servers/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name, owner})
    });
    const server = await res.json();
    alert(`Server created: ${server.name}`);
    fetchServers();
}

fetchServers();
