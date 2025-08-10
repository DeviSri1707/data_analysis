from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from processor import process_request
import aiofiles

app = FastAPI()

@app.post("/api/")
async def analyze_data(
    questions: UploadFile = File(...),
    files: list[UploadFile] = File(default=[])
):
    question_text = await questions.read()
    file_data = {}

    for file in files:
        content = await file.read()
        file_data[file.filename] = content

    result = await process_request(question_text.decode(), file_data)
    return JSONResponse(content=result)
