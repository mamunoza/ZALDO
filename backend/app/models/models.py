from __future__ import annotations

from datetime import datetime, date
from typing import Optional
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    JSON,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.orm import relationship
import uuid

from ..core.database import Base


JSONType = JSON().with_variant(SQLiteJSON(), "sqlite")


class User(Base):
    __tablename__ = "users"

    email_pk = Column(String, primary_key=True, index=True)
    nombre = Column(String, nullable=True)
    tz = Column(String, nullable=False, default="America/Santiago")
    moneda_base = Column(String, nullable=False, default="CLP")
    email_verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    flags = Column(JSONType, default=dict, nullable=False)

    accounts = relationship("Account", back_populates="owner")


class WaitlistEntry(Base):
    __tablename__ = "waitlist"

    email = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    source = Column(String, nullable=True)
    notes = Column(String, nullable=True)


class Invite(Base):
    __tablename__ = "invites"

    code = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by_email = Column(String, nullable=False)
    redeemed_by_email = Column(String, nullable=True)
    redeemed_at = Column(DateTime, nullable=True)
    max_uses = Column(Integer, default=1, nullable=False)
    uses = Column(Integer, default=0, nullable=False)


class Account(Base):
    __tablename__ = "accounts"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_email = Column(String, ForeignKey("users.email_pk"), nullable=False, index=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    institucion = Column(String, nullable=True)
    moneda = Column(String, nullable=False, default="CLP")

    owner = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_email = Column(String, ForeignKey("users.email_pk"), nullable=False, index=True)
    account_id = Column(PGUUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False, index=True)
    fecha_valor = Column(Date, nullable=False, index=True)
    fecha_contable = Column(Date, nullable=True)
    descripcion = Column(String, nullable=False)
    referencia = Column(String, nullable=True)
    monto_clp = Column(Numeric(14, 2), nullable=False)
    moneda_original = Column(String, nullable=True)
    monto_original = Column(Numeric(14, 2), nullable=True)
    categoria_id = Column(PGUUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    etiquetas = Column(JSONType, default=list, nullable=False)
    hash_dedup = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    account = relationship("Account", back_populates="transactions")
    categoria = relationship("Category", back_populates="transactions")

    __table_args__ = (
        UniqueConstraint("owner_email", "account_id", "fecha_valor", "hash_dedup", name="uq_transactions_hash"),
    )


class Category(Base):
    __tablename__ = "categories"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_email = Column(String, ForeignKey("users.email_pk"), nullable=False, index=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    padre_id = Column(PGUUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)

    transactions = relationship("Transaction", back_populates="categoria")


class Rule(Base):
    __tablename__ = "rules"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_email = Column(String, ForeignKey("users.email_pk"), nullable=False, index=True)
    nombre = Column(String, nullable=False)
    prioridad = Column(Integer, nullable=False, default=0)
    condiciones = Column(JSONType, nullable=False)
    acciones = Column(JSONType, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)


class UFValue(Base):
    __tablename__ = "uf_values"

    fecha = Column(Date, primary_key=True)
    valor_clp = Column(Numeric(10, 2), nullable=False)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_email = Column(String, ForeignKey("users.email_pk"), nullable=True)
    mensaje = Column(String, nullable=False)
    email_contacto = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ImportLog(Base):
    __tablename__ = "import_logs"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_email = Column(String, ForeignKey("users.email_pk"), nullable=False)
    account_id = Column(PGUUID(as_uuid=True), ForeignKey("accounts.id"), nullable=True)
    total_rows = Column(Integer, nullable=False)
    processed_rows = Column(Integer, nullable=False)
    duplicate_rows = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class MagicToken(Base):
    __tablename__ = "magic_tokens"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, index=True)
    token = Column(String, nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    used_at = Column(DateTime, nullable=True)

