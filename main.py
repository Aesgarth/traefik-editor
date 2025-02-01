from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from ruamel.yaml import YAML
from pathlib import Path
import shutil
import os
from datetime import datetime

# Initialize FastAPI app
app = FastAPI()

# Get the YAML file path from environment variables (default: /data/dynamic.yml)
CONFIG_FILE = os.getenv("CONFIG_FILE", "/data/dynamic.yml")
BACKUP_DIR = "backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

# Initialize ruamel.yaml
yaml = YAML()
yaml.preserve_quotes = True  # Preserve quotes and formatting
yaml.indent(mapping=2, sequence=4, offset=2)  # Ensures proper indentation


# Endpoint: Get YAML content (Return as a string instead of JSON)
@app.get("/config")
def get_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            yaml_content = file.read()  # Read YAML as a string (preserves comments)
        return {"yaml": yaml_content}  # Send as raw YAML instead of converting to JSON
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="YAML file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading YAML: {e}")


# Endpoint: Update YAML content (Preserve structure and comments)
@app.post("/config")
def update_config(new_yaml: dict):
    try:
        # Load existing YAML with comments
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                current_config = yaml.load(file)  # Preserve comments
        else:
            current_config = yaml.load("")  # Create an empty YAML structure

        # Backup the current file before modifying it
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path = os.path.join(BACKUP_DIR, f"dynamic-{timestamp}.yml")
        shutil.copy(CONFIG_FILE, backup_path)

        # Rotate backups (keep last 5)
        backups = sorted(os.listdir(BACKUP_DIR), reverse=True)
        if len(backups) > 5:
            for old_backup in backups[5:]:
                os.remove(os.path.join(BACKUP_DIR, old_backup))

        # Convert new input YAML (JSON payload) back into ruamel.yaml format
        updated_yaml = yaml.load(new_yaml["yaml"])  # Convert YAML string to ruamel's format

        # Write updated configuration back to file
        with open(CONFIG_FILE, "w") as file:
            yaml.dump(updated_yaml, file)

        return {"message": "Configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing YAML: {e}")


# Endpoint: List available backups
@app.get("/backups")
def list_backups():
    try:
        backups = sorted(os.listdir(BACKUP_DIR), reverse=True)
        return {"backups": backups}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing backups: {e}")


# Endpoint: Revert to a backup
class RevertRequest(BaseModel):
    backup_name: str

@app.post("/revert")
def revert_config(request: RevertRequest):
    try:
        backup_path = os.path.join(BACKUP_DIR, request.backup_name)
        if not os.path.exists(backup_path):
            raise HTTPException(status_code=404, detail="Backup not found")

        # Restore the backup
        shutil.copy(backup_path, CONFIG_FILE)
        return {"message": "Configuration reverted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error restoring backup: {e}")


# Serve the index.html page
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    try:
        with open("index.html") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="index.html not found")
    
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
