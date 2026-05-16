from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(64), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    display_name = Column(String(128), default="")
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    wallet_balance = Column(Float, default=0.0)
    api_key = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tasks = relationship("Task", back_populates="owner", cascade="all, delete")
    projects = relationship("Project", back_populates="owner")
    comments = relationship("Comment", back_populates="author")
    notifications = relationship("Notification", back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, default="")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, default="")
    status = Column(String(32), default="todo")
    priority = Column(Integer, default=1)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="tasks", foreign_keys=[owner_id])
    project = relationship("Project", back_populates="tasks")
    comments = relationship("Comment", back_populates="task", cascade="all, delete")
    attachments = relationship("Attachment", back_populates="task")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="comments")
    author = relationship("User", back_populates="comments")


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    filename = Column(String(512), nullable=False)
    stored_path = Column(String(1024), nullable=False)
    mime_type = Column(String(128), default="application/octet-stream")
    size_bytes = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="attachments")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(128), nullable=False)
    details = Column(Text, default="")
    ip_address = Column(String(64), default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class WebhookDelivery(Base):
    __tablename__ = "webhook_deliveries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_url = Column(String(2048), nullable=False)
    payload = Column(Text, nullable=False)
    status_code = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
