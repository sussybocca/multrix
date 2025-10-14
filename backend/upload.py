from fastapi import APIRouter, File, UploadFile, HTTPException, Form
import os
import hashlib

router = APIRouter()
UPLOAD_DIR = "storage/servers"
QUARANTINE_DIR = "storage/quarantine"

BLACKLIST_HASHES = set()

@router.post("/upload/")
async def upload_file(server_id: int = Form(...), file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(QUARANTINE_DIR, exist_ok=True)

    content = await file.read()
    sha256 = hashlib.sha256(content).hexdigest()

    if sha256 in BLACKLIST_HASHES:
        path = os.path.join(QUARANTINE_DIR, file.filename)
        with open(path, "wb") as f:
            f.write(content)
        raise HTTPException(status_code=403, detail="Malicious file detected!")

    # Save file in server folder
    server_folder = os.path.join(UPLOAD_DIR, str(server_id))
    os.makedirs(server_folder, exist_ok=True)
    path = os.path.join(server_folder, file.filename)
    with open(path, "wb") as f:
        f.write(content)

    # Update server files in memory
    from backend.main import servers
    for s in servers:
        if s.id == server_id:
            if file.filename not in s.files:
                s.files.append(file.filename)

    return {"filename": file.filename, "sha256": sha256, "status": "saved"}
