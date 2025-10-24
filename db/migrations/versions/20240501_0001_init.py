"""Initial schema

Revision ID: 20240501_0001
Revises:
Create Date: 2024-05-01
"""

from alembic import op
import sqlalchemy as sa
import uuid

revision = "20240501_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("email_pk", sa.String(), primary_key=True),
        sa.Column("nombre", sa.String(), nullable=True),
        sa.Column("tz", sa.String(), nullable=False, server_default="America/Santiago"),
        sa.Column("moneda_base", sa.String(), nullable=False, server_default="CLP"),
        sa.Column("email_verified_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("last_login_at", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("flags", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
    )

    op.create_table(
        "waitlist",
        sa.Column("email", sa.String(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("notes", sa.String(), nullable=True),
    )

    op.create_table(
        "invites",
        sa.Column("code", sa.String(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("created_by_email", sa.String(), nullable=False),
        sa.Column("redeemed_by_email", sa.String(), nullable=True),
        sa.Column("redeemed_at", sa.DateTime(), nullable=True),
        sa.Column("max_uses", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("uses", sa.Integer(), nullable=False, server_default="0"),
    )

    op.create_table(
        "accounts",
        sa.Column("id", sa.Uuid(), primary_key=True, default=uuid.uuid4),
        sa.Column("owner_email", sa.String(), sa.ForeignKey("users.email_pk"), nullable=False),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("tipo", sa.String(), nullable=False),
        sa.Column("institucion", sa.String(), nullable=True),
        sa.Column("moneda", sa.String(), nullable=False, server_default="CLP"),
    )

    op.create_table(
        "categories",
        sa.Column("id", sa.Uuid(), primary_key=True, default=uuid.uuid4),
        sa.Column("owner_email", sa.String(), sa.ForeignKey("users.email_pk"), nullable=False),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("tipo", sa.String(), nullable=False),
        sa.Column("padre_id", sa.Uuid(), sa.ForeignKey("categories.id"), nullable=True),
    )

    op.create_table(
        "rules",
        sa.Column("id", sa.Uuid(), primary_key=True, default=uuid.uuid4),
        sa.Column("owner_email", sa.String(), sa.ForeignKey("users.email_pk"), nullable=False),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("prioridad", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("condiciones", sa.JSON(), nullable=False),
        sa.Column("acciones", sa.JSON(), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.create_table(
        "uf_values",
        sa.Column("fecha", sa.Date(), primary_key=True),
        sa.Column("valor_clp", sa.Numeric(10, 2), nullable=False),
    )

    op.create_table(
        "feedback",
        sa.Column("id", sa.Uuid(), primary_key=True, default=uuid.uuid4),
        sa.Column("owner_email", sa.String(), sa.ForeignKey("users.email_pk"), nullable=True),
        sa.Column("mensaje", sa.String(), nullable=False),
        sa.Column("email_contacto", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "magic_tokens",
        sa.Column("id", sa.Uuid(), primary_key=True, default=uuid.uuid4),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("used_at", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "transactions",
        sa.Column("id", sa.Uuid(), primary_key=True, default=uuid.uuid4),
        sa.Column("owner_email", sa.String(), sa.ForeignKey("users.email_pk"), nullable=False),
        sa.Column("account_id", sa.Uuid(), sa.ForeignKey("accounts.id"), nullable=False),
        sa.Column("fecha_valor", sa.Date(), nullable=False),
        sa.Column("fecha_contable", sa.Date(), nullable=True),
        sa.Column("descripcion", sa.String(), nullable=False),
        sa.Column("referencia", sa.String(), nullable=True),
        sa.Column("monto_clp", sa.Numeric(14, 2), nullable=False),
        sa.Column("moneda_original", sa.String(), nullable=True),
        sa.Column("monto_original", sa.Numeric(14, 2), nullable=True),
        sa.Column("categoria_id", sa.Uuid(), sa.ForeignKey("categories.id"), nullable=True),
        sa.Column("etiquetas", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("hash_dedup", sa.String(), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_transactions_owner_account_date", "transactions", ["owner_email", "account_id", "fecha_valor"])

    op.create_table(
        "import_logs",
        sa.Column("id", sa.Uuid(), primary_key=True, default=uuid.uuid4),
        sa.Column("owner_email", sa.String(), sa.ForeignKey("users.email_pk"), nullable=False),
        sa.Column("account_id", sa.Uuid(), sa.ForeignKey("accounts.id"), nullable=True),
        sa.Column("total_rows", sa.Integer(), nullable=False),
        sa.Column("processed_rows", sa.Integer(), nullable=False),
        sa.Column("duplicate_rows", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("import_logs")
    op.drop_index("idx_transactions_owner_account_date", table_name="transactions")
    op.drop_table("transactions")
    op.drop_table("magic_tokens")
    op.drop_table("feedback")
    op.drop_table("uf_values")
    op.drop_table("rules")
    op.drop_table("categories")
    op.drop_table("accounts")
    op.drop_table("invites")
    op.drop_table("waitlist")
    op.drop_table("users")
