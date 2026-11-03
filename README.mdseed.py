from database import SessionLocal, engine, Base
import models

def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    d1 = models.Disease(
        disease_code="DISEASE-001",
        primary_name_ar="مرض السكري النوع الثاني",
        primary_name_en="Type 2 Diabetes Mellitus",
        icd11_code="5A11"
    )
    db.add(d1)
    db.commit()
    db.refresh(d1)
    
    sections_d1 = [
        models.DiseaseSection(
            disease_id=d1.id,
            section_key="التعريف والنظرة العامة",
            completeness_score="95%",
            content={"overview": "اضطراب استقلابي يتسم بارتفاع مستويات السكر في الدم نتيجة مقاومة الأنسولين.", "risk_factors": ["السمنة", "قلة النشاط البدني"]}
        ),
        models.DiseaseSection(
            disease_id=d1.id,
            section_key="التشخيص والمعايير",
            completeness_score="90%",
            content={"tests": ["فحص السكر التراكمي (HbA1c >= 6.5%)", "فحص السكر الصائم"], "symptoms": ["العطش الشديد", "كثرة التبول"]}
        )
    ]
    db.add_all(sections_d1)

    d2 = models.Disease(
        disease_code="DISEASE-002",
        primary_name_ar="ارتفاع ضغط الدم الأساسي",
        primary_name_en="Essential Hypertension",
        icd11_code="BA00"
    )
    db.add(d2)
    db.commit()
    db.refresh(d2)

    sections_d2 = [
        models.DiseaseSection(
            disease_id=d2.id,
            section_key="التعريف والنظرة العامة",
            completeness_score="90%",
            content={"overview": "حالة مزمنة تكون فيها قوة ضغط الدم على جدران الشرايين مرتفعة للغاية.", "target_reading": "أعلى من 130/80 ملم زئبق"}
        )
    ]
    db.add_all(sections_d2)

    db.commit()
    db.close()
    print("✅ تم إدراج البيانات الطبية الأولية بنجاح!")

if __name__ == "__main__":
    init_db()
