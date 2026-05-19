"""
Pydantic schemas for request / response validation.
Field names use camelCase to match the React frontend's JSON payloads.
- All inputs are validated for length, type, and format
- Email and phone validation enforced
"""

from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
import re


# ━━━━━━━━━━━━━━━━━━ Auth ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=255)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ━━━━━━━━━━━━━━━━━━ Popup ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class PopupBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=5000)
    isActive: bool = False
    image: str = Field("", max_length=2000000)

class PopupCreate(PopupBase):
    pass

class PopupUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=5000)
    isActive: Optional[bool] = None
    image: Optional[str] = Field(None, max_length=2000000)

class PopupOut(PopupBase):
    id: int
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# ━━━━━━━━━━━━━━━━━━ Testimonial ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestimonialBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    designation: str = Field("", max_length=200)
    description: str = Field(..., min_length=1, max_length=5000)
    rating: int = Field(5, ge=1, le=5)
    image: str = Field("", max_length=2000000)

class TestimonialCreate(TestimonialBase):
    pass

class TestimonialUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    designation: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=5000)
    rating: Optional[int] = Field(None, ge=1, le=5)
    image: Optional[str] = Field(None, max_length=2000000)

class TestimonialOut(TestimonialBase):
    id: int
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# ━━━━━━━━━━━━━━━━━━ Job Role ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class JobRoleBase(BaseModel):
    roleName: str = Field(..., min_length=1, max_length=200)
    qualification: str = Field("", max_length=2000)
    location: str = Field("", max_length=200)
    workCulture: str = Field("", max_length=2000)
    workTiming: str = Field("", max_length=200)
    description: str = Field("", max_length=5000)
    isActive: bool = True

class JobRoleCreate(JobRoleBase):
    pass

class JobRoleUpdate(BaseModel):
    roleName: Optional[str] = Field(None, min_length=1, max_length=200)
    qualification: Optional[str] = Field(None, max_length=2000)
    location: Optional[str] = Field(None, max_length=200)
    workCulture: Optional[str] = Field(None, max_length=2000)
    workTiming: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    isActive: Optional[bool] = None

class JobRoleOut(JobRoleBase):
    id: int
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# ━━━━━━━━━━━━━━━━━━ Intern Role ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class InternRoleBase(BaseModel):
    roleName: str = Field(..., min_length=1, max_length=200)

class InternRoleCreate(InternRoleBase):
    pass

class InternRoleOut(InternRoleBase):
    id: int
    createdAt: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# ━━━━━━━━━━━━━━━━━━ Client ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class ClientBase(BaseModel):
    companyName: str = Field(..., min_length=1, max_length=200)
    industry: str = Field("", max_length=200)
    description: str = Field("", max_length=5000)
    icon: str = Field("", max_length=2000000)

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    companyName: Optional[str] = Field(None, min_length=1, max_length=200)
    industry: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    icon: Optional[str] = Field(None, max_length=2000000)

class ClientOut(ClientBase):
    id: int
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# ━━━━━━━━━━━━━━━━━━ Team Member ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TeamMemberBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    role: str = Field("", max_length=200)
    avatar: str = Field("", max_length=2000000)
    bio: str = Field("", max_length=2000)

class TeamMemberCreate(TeamMemberBase):
    pass

class TeamMemberUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    role: Optional[str] = Field(None, max_length=200)
    avatar: Optional[str] = Field(None, max_length=2000000)
    bio: Optional[str] = Field(None, max_length=2000)

class TeamMemberOut(TeamMemberBase):
    id: int
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# ━━━━━━━━━━━━━━━━━━ Contact ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class ContactBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: str = Field("", max_length=20)
    subject: str = Field("", max_length=500)
    message: str = Field(..., min_length=1, max_length=10000)
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v and not re.match(r'^[\d+\-\s\(\)]{7,20}$', v):
            raise ValueError('Phone must be 7-20 characters with digits, +, -, spaces, or parentheses')
        return v

class ContactCreate(ContactBase):
    pass

class ContactOut(ContactBase):
    id: int
    isRead: bool = False
    createdAt: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# ━━━━━━━━━━━━━━━━━━ Job Application ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class JobApplicationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: str = Field("", max_length=20)
    address: str = Field("", max_length=500)
    location: str = Field("", max_length=200)
    qualification: str = Field("", max_length=2000)
    experience: str = Field("", max_length=2000)
    message: str = Field("", max_length=10000)
    resume: str = Field("", max_length=100000)
    resumeName: str = Field("", max_length=255)
    resumeType: str = Field("", max_length=255)
    jobRole: str = Field(..., min_length=1, max_length=200)
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v and not re.match(r'^[\d+\-\s\(\)]{7,20}$', v):
            raise ValueError('Phone must be 7-20 characters with digits, +, -, spaces, or parentheses')
        return v

class JobApplicationCreate(JobApplicationBase):
    pass

class JobApplicationUpdate(BaseModel):
    status: Optional[str] = Field(None, max_length=50)
    isRead: Optional[bool] = None

class JobApplicationOut(JobApplicationBase):
    id: int
    status: str = "Pending"
    isRead: bool = False
    createdAt: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# ━━━━━━━━━━━━━━━━━━ Intern Application ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class InternApplicationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: str = Field("", max_length=20)
    role: str = Field("", max_length=200)
    address: str = Field("", max_length=500)
    qualification: str = Field("", max_length=2000)
    skills: str = Field("", max_length=2000)
    duration: str = Field("3 Months", max_length=100)
    message: str = Field("", max_length=10000)
    resume: str = Field("", max_length=100000)
    resumeName: str = Field("", max_length=255)
    resumeType: str = Field("", max_length=255)
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v and not re.match(r'^[\d+\-\s\(\)]{7,20}$', v):
            raise ValueError('Phone must be 7-20 characters with digits, +, -, spaces, or parentheses')
        return v

class InternApplicationCreate(InternApplicationBase):
    pass

class InternApplicationUpdate(BaseModel):
    status: Optional[str] = Field(None, max_length=50)
    isRead: Optional[bool] = None

class InternApplicationOut(InternApplicationBase):
    id: int
    status: str = "Pending"
    isRead: bool = False
    createdAt: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# ━━━━━━━━━━━━━━━━━━ Project Inquiry (Get Started) ━━━━━━━━━━━━━━━━━━━
class ProjectInquiryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: str = Field("", max_length=20)
    company: str = Field("", max_length=200)
    selectedServices: List[str] = Field(default_factory=list, max_length=50)
    budget: str = Field("", max_length=100)
    timeline: str = Field("", max_length=200)
    projectDetails: str = Field("", max_length=10000)
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v and not re.match(r'^[\d+\-\s\(\)]{7,20}$', v):
            raise ValueError('Phone must be 7-20 characters with digits, +, -, spaces, or parentheses')
        return v

class ProjectInquiryCreate(ProjectInquiryBase):
    pass

class ProjectInquiryUpdate(BaseModel):
    status: Optional[str] = Field(None, max_length=50)
    isRead: Optional[bool] = None

class ProjectInquiryOut(ProjectInquiryBase):
    id: int
    status: str = "New"
    isRead: bool = False
    createdAt: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# ━━━━━━━━━━━━━━━━━━ Site Photo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class SitePhotoBase(BaseModel):
    url: str = Field(..., min_length=1, max_length=2000000)
    name: str = Field("", max_length=255)
    alt: str = Field("", max_length=500)

class SitePhotoCreate(SitePhotoBase):
    pass

class SitePhotoOut(SitePhotoBase):
    id: int
    createdAt: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


# ━━━━━━━━━━━━━━━━━━ Portfolio ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class PortfolioBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    category: str = Field("", max_length=100)
    description: str = Field("", max_length=5000)
    image: str = Field("", max_length=2000000)
    tags: List[str] = Field(default_factory=list, max_length=50)
    clientName: str = Field("", max_length=200)

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=5000)
    image: Optional[str] = Field(None, max_length=2000000)
    tags: Optional[List[str]] = Field(None, max_length=50)
    clientName: Optional[str] = Field(None, max_length=200)

class PortfolioOut(PortfolioBase):
    id: int
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
