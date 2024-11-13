from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from minio.error import S3Error
from minio import Minio
from utils import config

router = APIRouter(prefix="/minio", tags=["Minio"])

minio_client = Minio(
    config.MINIO_ENDPOINT,
    access_key=config.MINIO_ACCESS_KEY,
    secret_key=config.MINIO_SECRET_KEY,
    cert_check=False,
    secure=False,
)
minio_bucket = config.MINIO_BUCKET


@router.get("/")
def list_objects():
    objects = minio_client.list_objects(minio_bucket)
    results = []
    for obj in objects:
        obj_data = minio_client.stat_object(minio_bucket, obj.object_name)
        results.append(obj_data)
    return {"objects": results}


@router.post("/upload")
async def upload_object(file: UploadFile):
    try:
        minio_client.put_object(
            bucket_name=minio_bucket,
            object_name=file.filename,
            data=file.file,
            length=-1,
            part_size=10 * 1024 * 1024,
        )

        return {"message": "File uploaded successfully"}
    except Exception as e:
        return {"error": str(e)}


@router.post("/download")
def download_object(filename: str):
    try:
        file_data = minio_client.get_object(minio_bucket, filename)
        return StreamingResponse(
            file_data,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except S3Error as e:
        raise HTTPException(status_code=404, detail=f"File not found: {str(e)}")
