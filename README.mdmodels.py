from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    disease_code = Column(String, unique=True, index=True, nullable=False)
    primary_name_ar = Column(String, nullable=False)
    primary_name_en = Column(String, nullable=True)
    icd11_code = Column(String, nullable=True)

    sections = relationship("DiseaseSection", back_populates="disease", cascade="all, delete-orphan")

class DiseaseSection(Base):
    __tablename__ = "disease_sections"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"), nullable=False)
    section_key = Column(String, nullable=False)
    completeness_score = Column(String, default="0%")
    content = Column(JSON, nullable=False)

    disease = relationship("Disease", back_populates="sections")
