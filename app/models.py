from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, Date, DateTime
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Environment(str, Enum):
    DEV = "DEV"
    STAGE = "STAGE"
    PROD = "PROD"


class SnapshotType(str, Enum):
    BEFORE = "BEFORE"
    AFTER = "AFTER"


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    patch_events = relationship("PatchEvent", back_populates="service")


class PatchEvent(Base):
    __tablename__ = "patch_events"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(
        Integer,
        ForeignKey("services.id"),
        nullable=False,
        index=True,
    )
    environment = Column(SAEnum(Environment), nullable=False)
    ami_id = Column(String(64), nullable=False)
    patch_date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)
    dev_evidence_available = Column(Boolean, default=False, nullable=False)
    stage_cr_summary = Column(Text, nullable=True)
    prod_cr_summary = Column(Text, nullable=True)
    current_state_code = Column(
        String(50),
        nullable=False,
        default="DEV_EVIDENCE_CAPTURED",
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    service = relationship("Service", back_populates="patch_events")
    snapshots = relationship(
        "ScanSnapshot",
        back_populates="patch_event",
        cascade="all, delete-orphan",
    )


class ScanSnapshot(Base):
    __tablename__ = "scan_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    patch_event_id = Column(
        Integer,
        ForeignKey("patch_events.id"),
        nullable=False,
        index=True,
    )
    snapshot_type = Column(SAEnum(SnapshotType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    patch_event = relationship("PatchEvent", back_populates="snapshots")
    vulnerabilities = relationship(
        "Vulnerability",
        back_populates="scan_snapshot",
        cascade="all, delete-orphan",
    )


class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    scan_snapshot_id = Column(
        Integer,
        ForeignKey("scan_snapshots.id"),
        nullable=False,
        index=True,
    )
    synthetic_id = Column(String(50), nullable=False)
    cve = Column(String(20), nullable=True)
    plugin_id = Column(String(20), nullable=True)
    severity = Column(SAEnum(Severity), nullable=False)
    host = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    scan_snapshot = relationship(
        "ScanSnapshot",
        back_populates="vulnerabilities",
    )
