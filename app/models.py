"""
SQLAlchemy ORM models – one table per frontend entity.

Tables:
  popups, testimonials, job_roles, intern_roles, clients, team_members,
  contacts, job_applications, intern_applications, project_inquiries,
  site_photos, portfolios
"""

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Float, DateTime, JSON
)
from sqlalchemy.sql import func
from app.database import Base


# ── Popups ─────────────────────────────────────────────────────────────
class Popup(Base):
    __tablename__ = "popups"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    is_active = Column(Boolean, default=False)
    image = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ── Testimonials ───────────────────────────────────────────────────────
class Testimonial(Base):
    __tablename__ = "testimonials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    designation = Column(String(255), default="")
    description = Column(Text, nullable=False)
    rating = Column(Integer, default=5)
    image = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ── Job Roles ──────────────────────────────────────────────────────────
class JobRole(Base):
    __tablename__ = "job_roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(255), nullable=False)
    qualification = Column(String(255), default="")
    location = Column(String(255), default="")
    work_culture = Column(String(100), default="")
    work_timing = Column(String(100), default="")
    description = Column(Text, default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ── Intern Roles ───────────────────────────────────────────────────────
class InternRole(Base):
    __tablename__ = "intern_roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ── Clients ────────────────────────────────────────────────────────────
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False)
    industry = Column(String(255), default="")
    description = Column(Text, default="")
    icon = Column(Text, default="")          # URL or base64
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ── Team Members ───────────────────────────────────────────────────────
class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    role = Column(String(255), default="")
    avatar = Column(Text, default="")        # URL or initials
    bio = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ── Contacts (from contact form) ──────────────────────────────────────
class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), default="")
    subject = Column(String(255), default="")
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ── Job Applications ──────────────────────────────────────────────────
class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), default="")
    address = Column(Text, default="")
    location = Column(Text, default="")
    qualification = Column(String(255), default="")
    experience = Column(String(100), default="")
    message = Column(Text, default="")
    resume = Column(Text, default="")         # base64 data
    resume_name = Column(String(255), default="")
    resume_type = Column(String(255), default="")
    job_role = Column(String(255), nullable=False)
    status = Column(String(50), default="Pending")
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ── Intern Applications ───────────────────────────────────────────────
class InternApplication(Base):
    __tablename__ = "intern_applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), default="")
    role = Column(String(255), default="")
    address = Column(Text, default="")
    qualification = Column(String(255), default="")
    skills = Column(String(500), default="")
    duration = Column(String(50), default="3 Months")
    message = Column(Text, default="")
    resume = Column(Text, default="")
    resume_name = Column(String(255), default="")
    resume_type = Column(String(255), default="")
    status = Column(String(50), default="Pending")
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ── Project Inquiries (GetStarted form) ───────────────────────────────
class ProjectInquiry(Base):
    __tablename__ = "project_inquiries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), default="")
    company = Column(String(255), default="")
    selected_services = Column(JSON, default=[])   # list of service IDs
    budget = Column(String(100), default="")
    timeline = Column(String(100), default="")
    project_details = Column(Text, default="")
    status = Column(String(50), default="New")
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ── Site Photos ────────────────────────────────────────────────────────
class SitePhoto(Base):
    __tablename__ = "site_photos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=False)
    name = Column(String(255), default="")
    alt = Column(String(255), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ── Portfolio Projects ─────────────────────────────────────────────────
class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), default="")
    description = Column(Text, default="")
    image = Column(Text, default="")
    tags = Column(JSON, default=[])
    client_name = Column(String(255), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
