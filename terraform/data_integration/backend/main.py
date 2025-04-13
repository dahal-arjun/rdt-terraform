from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from pydantic import BaseModel
import boto3
from botocore.exceptions import NoCredentialsError
from typing import Dict
import uvicorn
import random
import requests
from datetime import datetime
try:
    from database import engine, SessionLocal
    import models
    from models import Session, Cryptography
except:
    from data_integration.backend.database import engine, SessionLocal
    import data_integration.backend.models as models
    from data_integration.backend.models import Session, Cryptography


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

ACCESS_KEY = 'AKIAVVDNZERRFW47TJG6'
SECRET_KEY = '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'
BUCKET_NAME = 'rightdataspark'
FOLDER_PATH = 'scripts/'
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class IngestionParams(BaseModel):
    notebook_params: Dict[str, str] = {None}
    
    class Config:
        json_schema_extra = {
            "example": {
                "notebook_params": {
                    "notebook_name": "notebook_name",
                    "master_url": "master_url",
                }
            }
        }
    
class CryptographyParams(BaseModel):
    scope: str = None
    iv: str = None
    salt: str = None
    iteration: int = None
    length: int = None
    password: str = None
    
class ScopeParams(BaseModel):
    scope: str = None


def jobrun(notebook_params, submission_id):
    result = [f"/home/ec2-user/data_integration/scripts/{notebook_params['notebook_name']}.py"]
    for key, value in notebook_params.items():
        result.extend(['--' + key, value])
    result.extend(['--submission_id', str(submission_id)])
    payload = {
        "appResource": f"/home/ec2-user/data_integration/scripts/{notebook_params['notebook_name']}.py",
        "sparkProperties": {
            "spark.master": f"spark://{notebook_params['master_url']}:7077",
            "spark.app.name": "Spark REST API - PI",
            "spark.submit.deployMode": "client"
        },
        "clientSparkVersion": "3.5.0",
        "mainClass": "org.apache.spark.deploy.SparkSubmit",
        "environmentVariables": {
            "SPARK_ENV_LOADED": "1"
        },
        "action": "CreateSubmissionRequest",
        "appArgs": result
    }
    
    url = f"http://{notebook_params['master_url']}:6066/v1/submissions/create"
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()['submissionId']
    
def jobrun_with_s3(notebook_params, submission_id):
    print(notebook_params)
    result = [f"https://rightdataspark.s3.us-east-1.amazonaws.com/scripts/{notebook_params['notebook_name']}.py"]
    for key, value in notebook_params.items():
        result.extend(['--' + key, value])
    result.extend(['--submission_id', str(submission_id)])
    payload = {
        "appResource": f"https://rightdataspark.s3.us-east-1.amazonaws.com/scripts/{notebook_params['notebook_name']}.py",
        "sparkProperties": {
            "spark.master": f"spark://{notebook_params['master_url']}:7077",
            "spark.app.name": "Spark REST API - PI",
            "spark.submit.deployMode": "client"
        },
        "clientSparkVersion": "3.5.0",
        "mainClass": "org.apache.spark.deploy.SparkSubmit",
        "environmentVariables": {
            "SPARK_ENV_LOADED": "1"
        },
        "action": "CreateSubmissionRequest",
        "appArgs": result
    }
    url = f"http://{notebook_params['master_url']}:6066/v1/submissions/create"
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()['submissionId']

@app.post("/run_ingestion_s3")
def submit_ingestion(params: IngestionParams, db=Depends(get_db)):
    print(params)
    try:
        submission_id = "submission_" + datetime.now().strftime("%Y%m%d%H%M%S")
        driver_id = jobrun_with_s3(params.notebook_params, submission_id)
        session = Session(id=str(submission_id), driver_id=driver_id)
        db.add(session)
        db.commit()
        db.refresh(session)
        return {"submission_id": submission_id, "driver_id": driver_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/run_ingestion_server")
def submit_ingestion_server(params: IngestionParams, db=Depends(get_db)):
    print(params)
    try:
        submission_id = "submission_" + datetime.now().strftime("%Y%m%d%H%M%S")
        driver_id = jobrun(params.notebook_params, submission_id)
        session = Session(id=str(submission_id), driver_id=driver_id)
        db.add(session)
        db.commit()
        db.refresh(session)
        return {"submission_id": submission_id, "driver_id": driver_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/add_scope")
def add_scope(params: ScopeParams, db=Depends(get_db)):
    try:
        scope = params.scope
        scope = Cryptography(scope=scope)
        db.add(scope)
        db.commit()
        db.refresh(scope)
        return {"scope": scope.scope}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/add_secrets")
def add_secrets(params: CryptographyParams, db=Depends(get_db)):
    try:
        scope = params.scope
        iv = params.iv
        salt = params.salt
        iteration = params.iteration
        length = params.length
        password = params.password
        cryptography = models.Cryptography(scope=scope, iv=iv, salt=salt, iteration=iteration, length=length, password=password)
        db.add(cryptography)
        db.commit()
        db.refresh(cryptography)
        return {"message": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/get_secrets")
def get_secrets(scope: str, db=Depends(get_db)):
    try:
        cryptography = db.query(Cryptography).filter(Cryptography.scope == scope).first()
        return {"iv": cryptography.iv, "salt": cryptography.salt, "iteration": cryptography.iteration, "length": cryptography.length, "password": cryptography.password}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/upload_file_to_s3")
def upload_file_to_s3(file: UploadFile = File(...)):
    try:
        s3.upload_fileobj(file.file, BUCKET_NAME, FOLDER_PATH + file.filename)
        return {"message": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/list_files_in_s3")
def list_files_in_s3_without_folder_path():
    try:
        contents = s3.list_objects(Bucket=BUCKET_NAME, Prefix=FOLDER_PATH)['Contents']
        files = [content['Key'].split('/')[-1].split('.')[0] for content in contents]
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":

    uvicorn_config = {
        "app": "main:app",
        "host": "0.0.0.0",
        "port": 8000,
        "reload": False,
        "workers": 4
    }

    uvicorn.run("app:app", **uvicorn_config)