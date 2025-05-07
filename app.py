from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import os, time

app = FastAPI(debug=True)

video_save_path = "C:\\Users\\vipla\\Desktop\\pdf_renamer\\files\\"


class FileMeta(BaseModel):
    id: int
    filename: str
    content_type: str


@app.get("/")
async def root():
    
    return "write /docs"
  
@app.get("/files")
async def list_of_files():
    data = os.listdir(video_save_path)
    all_data = []
    if (len(data)>=1):
        for i in range(len(data)):
            # Get file creation and modification times
            file_stat = os.stat(video_save_path+data[i])
            creation_time = time.ctime(file_stat.st_ctime)
            modification_time = time.ctime(file_stat.st_mtime)
            all_data.append({"filename":data[i], "file_id":i, "creation_time":creation_time, "modification_time":modification_time})
        return {"message":"successfully get the data", "data":all_data, "status":200}
    else:
        return {"message":"there is no file in the provided directory", "data":[], "status":404}
    
@app.post("/upload", response_model=FileMeta)
async def upload_file(file: UploadFile = File(...)):
    # Save the file to the disk
    file_location = f"{video_save_path}\\{file.filename}"
    try:
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        return {"message":"uploading successful", "status":200}
    except:
        return {"message":"uploading unsuccessful", "status":404}

# slash before is important but after it will consider as name
@app.delete("/delete")
async def delete_file(filename):
    try:
        os.remove(video_save_path+filename)
        return {"message": f"File '{filename}' deleted","status":200}
    except:
        return {"message": f"File '{filename}' not found","status":404}
    

# this will be /rename_file?number of arguments we define in below function
@app.get("/rename_file")
async def file_rename(oldname, newname):  # these became input field inside browser
    try:
        os.rename(video_save_path+oldname, f"{video_save_path}{newname}")
        return {"message": "file renamed","status":200}
    except:
        return {"message": "file not found","status":404}

@app.get("/search")
async def search_file(search):
    files = os.listdir(video_save_path)
    retlist = []
    for filename in files:
        if search.lower() in filename.lower():
            file_stat = os.stat(video_save_path+filename)
            print(file_stat)
            creation_time = time.ctime(file_stat.st_ctime)
            modification_time = time.ctime(file_stat.st_mtime)
            retlist.append({"filename":filename, "creation_time":creation_time, "modification_time":modification_time})
    if retlist:
        return {"massage":"searching data find","data":retlist,"status":200}
    else:
        return {"massage":"unable to find","data":[],"status":404}
    
    # return [file for filename in files if search in filename.lower()]
