from fastapi import APIRouter, Depends, UploadFile,WebSocket,WebSocketDisconnect,Query
from typing import Annotated
from task.file_processing import process_file
from .user import validate_token
from firebase_admin.auth import verify_id_token
import shutil
import asyncio
from pathlib import Path
from tempfile import NamedTemporaryFile
import os
import redis
import json

router = APIRouter()


def save_upload_file_tmp(upload_file: UploadFile, user_id) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        path = Path(f"{os.environ['TMP_FOLDER']}{user_id}")
        path.mkdir(parents=True)

        with NamedTemporaryFile(dir=path, delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp.name


@router.post("/uploadfile")
def create_upload_file(
    file: UploadFile, user_id: Annotated[str, Depends(validate_token)]
):
    path = save_upload_file_tmp(file,user_id)
    task = process_file.delay(path, user_id)
    return {"task_id": task.id, "status": "processing"}


redis_client = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)


@router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket, user_id:str):
    try:
        user_id = verify_id_token(user_id)['user_id']
        await websocket.accept()
        pubsub = redis_client.pubsub()
        pubsub.subscribe(user_id)

        print(f"WebSocket connection established for user {user_id}")

        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)
            if message and message["type"] == "message":
                data = json.loads(message["data"])
                await websocket.send_json(data)
                if float(data['progress']) >= 100:
                    break
            await asyncio.sleep(0.1)
        print("end")
        websocket.close()
        return {"progress":"complete"}

    except WebSocketDisconnect:
        print(f"User {user_id} disconnected.")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close(code=1011)
