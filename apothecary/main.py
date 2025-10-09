from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from apothecary.auditor.explain import (
    explain_label_skew,
    explain_length_outlier,
    explain_backdoor
)
from apothecary.schemas import Prompt, ScanOut, AuditOut
from apothecary.scanner.heuristic import heuristic_score
from apothecary.scanner.classifier import model_score
from apothecary.auditor.dataset import audit_csv
from sklearn.neighbors import LocalOutlierFactor
import pandas as pd
import tempfile
import os
import csv
import io

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

@app.post("/audit/poison-csv")
def poison_csv(file: UploadFile = File(...)):
    """Return only poison rows + reasons as CSV."""
    df = pd.read_csv(file.file)                      # same loader
    label_col = df.columns[-1]
    vc = df[label_col].value_counts(normalize=True)
    skew_flag = (vc.max() > 0.95)
    skew_expl = explain_label_skew(vc.to_dict()) if skew_flag else ""

    lengths = df["text"].str.len()
    mean, std = lengths.mean(), lengths.std()
    lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
    outlier_mask = lof.fit_predict(lengths.values.reshape(-1, 1)) == -1

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["text", "label", "reason"])

    for idx, row in df.iterrows():
        reasons = []
        if skew_flag:
            reasons.append(skew_expl)
        if outlier_mask[idx]:
            reasons.append(explain_length_outlier(lengths.iloc[idx], mean, std))
        back_reason = explain_backdoor(row["text"])
        if back_reason:
            reasons.append(back_reason)

        if reasons:
            writer.writerow([row["text"], row[label_col], " | ".join(reasons)])

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=poison_report.csv"}
    )
