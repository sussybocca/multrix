from fastapi import APIRouter, HTTPException
import subprocess
import os

router = APIRouter()

SERVER_DIR = "storage/servers"

@router.post("/sandbox/run/{server_id}")
async def run_code(server_id: int, filename: str):
    path = os.path.join(SERVER_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        # Run Python code in subprocess safely (sandbox stub)
        result = subprocess.run(
            ["python3", path],
            capture_output=True,
            timeout=5,
            text=True
        )
        return {"stdout": result.stdout, "stderr": result.stderr}
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Execution timed out"}
