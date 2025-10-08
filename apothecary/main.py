from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from apothecary.schemas import Prompt, ScanOut, AuditOut
from apothecary.scanner.heuristic import heuristic_score
from apothecary.scanner.classifier import model_score
from apothecary.auditor.dataset import audit_csv
import pandas as pd
import tempfile
import os

app = FastAPI(title="ApothecaryAI-local")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)          # serve the SPA
def spa():
    with open("static/index.html", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/scan", response_model=ScanOut)
def scan(payload: Prompt):
    h = heuristic_score(payload.text)
    m = model_score(payload.text)
    score = max(h, m)               # ensemble: either can flag
    flagged = score > 0.5
    reason = "heuristic" if h > m else "model"
    return ScanOut(prompt=payload.text, score=score,
                   flagged=flagged, reason=reason)

@app.post("/audit/dataset", response_model=AuditOut)
def audit(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1]
    if suffix not in {".csv"}:
        raise HTTPException(status_code=400, detail="Only CSV supported")
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(file.file.read())
        tmp.flush()
        result = audit_csv(tmp.name)
    os.unlink(tmp.name)
    return AuditOut(**result)

@app.post("/audit/report", response_model=AuditOut) # same logic, new URL
def audit_report(file: UploadFile = File(...)):
    return audit(file)          # re-use existing audit endpoint