from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from models import Server
from state import servers
from upload import router as upload_router
from sandbox import router as sandbox_router
import io
import sys

app = FastAPI(title="Multrix")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hardcoded API key
API_KEY = "aksth$5:&@dfhafkotn"

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

# --- Python code execution endpoint ---
class CodeRequest(BaseModel):
    code: str

@app.post("/run-python")
async def run_python(req: CodeRequest):
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    try:
        exec(req.code, {"__builtins__": {}})
    except Exception as e:
        sys.stdout = old_stdout
        return JSONResponse(content={"error": str(e)})
    sys.stdout = old_stdout
    return {"output": redirected_output.getvalue()}

# --- API key endpoint ---
@app.get("/get-api-key")
async def get_api_key():
    return {"api_key": API_KEY}

# --- Serve frontend from root ---
app.mount("/", StaticFiles(directory=".", html=True), name="frontend")

# Optional explicit root route for index.html
@app.get("/")
async def root():
    return FileResponse("index.html")