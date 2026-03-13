

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from validator import validate_image
from tamper import tamper_analysis
from ocr import analyze_ocr   # ← OCR module

app = FastAPI(title="ID Forgery Detection API")


@app.post("/analyze-id")
async def analyze_id(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()

    
        is_valid, message = validate_image(file_bytes)

        if not is_valid:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "failed",
                    "stage": "validation",
                    "filename": file.filename,
                    "reason": message
                }
            )

  
        tamper_report = tamper_analysis(file_bytes)


        ocr_report = analyze_ocr(file_bytes)


        return {
            "status": "success",
            "filename": file.filename,
            "content_type": file.content_type,
            "validation": message,
            "tampering_analysis": tamper_report,
            "ocr_analysis": ocr_report
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "detail": str(e)
            }
        )