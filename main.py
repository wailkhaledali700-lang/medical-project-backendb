from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional

from database import SessionLocal, engine
import models

app = FastAPI(
    title="المشروع الطبي 1357 API",
    version="4.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/diseases/search")
def search_diseases(query: Optional[str] = Query(None), db: Session = Depends(get_db)):
    if not query:
        return {"status": "success", "data": []}
    
    search_term = f"%{query}%"
    diseases = db.query(models.Disease).filter(
        (models.Disease.primary_name_ar.ilike(search_term)) |
        (models.Disease.primary_name_en.ilike(search_term)) |
        (models.Disease.disease_code.ilike(search_term))
    ).all()
    
    results = []
    for d in diseases:
        results.append({
            "disease_code": d.disease_code,
            "primary_name_ar": d.primary_name_ar,
            "primary_name_en": d.primary_name_en,
            "icd11_code": d.icd11_code
        })
        
    return {"status": "success", "count": len(results), "data": results}

@app.get("/api/diseases/{disease_code}")
def get_disease_details(disease_code: str, db: Session = Depends(get_db)):
    disease = db.query(models.Disease).filter(models.Disease.disease_code == disease_code.upper()).first()
    
    if not disease:
        raise HTTPException(status_code=404, detail="لم يتم العثور على المرض المطلوبة")
        
    sections_data = []
    for s in disease.sections:
        sections_data.append({
            "section_key": s.section_key,
            "completeness_score": s.completeness_score,
            "content": s.content
        })
        
    response_data = {
        "disease_code": disease.disease_code,
        "primary_name_ar": disease.primary_name_ar,
        "primary_name_en": disease.primary_name_en,
        "icd11_code": disease.icd11_code,
        "disease_sections": sections_data
    }
    
    return {"status": "success", "data": response_data}
