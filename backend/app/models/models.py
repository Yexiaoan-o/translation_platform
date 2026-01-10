from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.models.db import Base

# 状态枚举
class SegmentStatus(str, enum.Enum):
    UNTRANSLATED = "untranslated"
    EDITED = "edited"
    CONFIRMED = "confirmed"
    LOCKED = "locked"

# 项目表
class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    source_language = Column(String(10), nullable=False)
    target_language = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    segments = relationship("Segment", back_populates="project", cascade="all, delete-orphan")
    files = relationship("ProjectFile", back_populates="project", cascade="all, delete-orphan")

# 项目文件表
class ProjectFile(Base):
    __tablename__ = "project_files"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_type = Column(String(50), nullable=False)
    
    # 关系
    project = relationship("Project", back_populates="files")

# 翻译段落表
class Segment(Base):
    __tablename__ = "segments"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    source_text = Column(Text, nullable=False)
    target_text = Column(Text, nullable=True)
    status = Column(Enum(SegmentStatus), default=SegmentStatus.UNTRANSLATED)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    project = relationship("Project", back_populates="segments")

# 术语表
class Term(Base):
    __tablename__ = "terms"
    
    id = Column(Integer, primary_key=True, index=True)
    source_term = Column(String(255), nullable=False)
    target_term = Column(String(255), nullable=False)
    source_language = Column(String(10), nullable=False)
    target_language = Column(String(10), nullable=False)
    domain = Column(String(100), nullable=True)
    definition = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 翻译记忆表
class TranslationMemory(Base):
    __tablename__ = "translation_memories"
    
    id = Column(Integer, primary_key=True, index=True)
    source_text = Column(Text, nullable=False)
    target_text = Column(Text, nullable=False)
    source_language = Column(String(10), nullable=False)
    target_language = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)