from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from models import Server
from state import servers
from upload import router as upload_router
from sandbox import router as sandbox_router

app = FastAPI(title="Multrix")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# --- Include routers ---
app.include_router(upload_router)
app.include_router(sandbox_router)

# --- Serve frontend ---
app.mount("/static", StaticFiles(directory=".", html=True), name="frontend")

@app.get("/")
async def root():
    return FileResponse("index.html")
