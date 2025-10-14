from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from models import Server  # <- changed from backend.models

app = FastAPI(title="Multrix")

# Allow frontend to call backend (for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory servers
servers = [
    Server(id=1, name="Example Server 1", owner="Alice", description="Demo server", files=[]),
    Server(id=2, name="Example Server 2", owner="Bob", description="Another demo", files=[])
]

# JSON model for creating server
class ServerCreateRequest(BaseModel):
    name: str
    owner: str

# --- Backend API ---

@app.get("/servers")
async def list_servers():
    return [s.dict() for s in servers]

@app.post("/servers/create")
async def create_server(req: ServerCreateRequest):
    new_id = max([s.id for s in servers] + [0]) + 1
    server = Server(id=new_id, name=req.name, owner=req.owner, files=[])
    servers.append(server)
    return server.dict()

@app.get("/servers/{server_id}")
async def get_server(server_id: int):
    for s in servers:
        if s.id == server_id:
            return s.dict()
    return {"error": "Server not found"}

# --- Serve frontend from root ---
app.mount("/", StaticFiles(directory=".", html=True), name="frontend")
