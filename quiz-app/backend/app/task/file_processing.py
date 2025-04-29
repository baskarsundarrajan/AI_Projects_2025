from fastapi import UploadFile
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable
from utils.pdf_vectorizer import PDFVectorizer
from core.vector_operations import VectorDBOperations as db
from core.config.celery_config import celery
import os


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
    return tmp_path


def handle_upload_file(tmp_path: str, handler: Callable[[Path], None]) -> None:
    try:
        tmp_path = Path(tmp_path)
        chunks = handler(tmp_path)
    finally:
        tmp_path.unlink()
        shutil.rmtree(tmp_path.parent)
    return chunks


@celery.task(name="task.file_processing.process_file")
def process_file(file, user_id):
    pdf_vectorizer = PDFVectorizer()
    chunks = handle_upload_file(file, pdf_vectorizer.pdf_vectorize_store)
    client = db.connect_weaviate()
    db.delete(client,user_id)
    db.insert(client, chunks, user_id)
    client.close()
    print("Done hehe")
    return {"filename": "processing compelete"}
