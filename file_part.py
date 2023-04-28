from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import FileResponse
import aiohttp
import pymongo
import gridfs
import aiofiles

app = FastAPI()

#client = pymongo.MongoClient("mongodb+srv://root:Kukakuka0078@cluster0.242xx9v.mongodb.net/?retryWrites=true&w=majority")
client = pymongo.MongoClient("localhost:8080")

db = client["mydatabase"]
fs = gridfs.GridFS(db)

@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    existing_file = fs.find_one({"filename": file.filename})
    if existing_file:
        # If file with same name exists, delete it
        fs.delete(existing_file._id)

    # Upload new file
    #file_id = fs.put(file, filename=filename)

    fs.put(file.file, filename=file.filename)  # async write
    
    #ext_t=file.filename.split('.')

    return{"filename" : file.filename}
    
    #return {'hello' : 'hello'}

@app.get("/search_file/")
async def search_file(filename: str):
    docs = fs.find({"filename": filename})
    doc_ids = [str(doc._id) for doc in docs]
    if len(doc_ids) > 0:
        return {"message": "File found with ID(s): " + ", ".join(doc_ids)}
    else:
        return {"message": "File not found."}

@app.get("/download_file/")
async def download_file(filename: str):
    file_doc = fs.find_one({"filename": filename})
    if not file_doc:
        return {"message": "File not found."}

    #Download file and return as response
    file_data = fs.get(file_doc._id).read()
    response = Response(content=file_data)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response