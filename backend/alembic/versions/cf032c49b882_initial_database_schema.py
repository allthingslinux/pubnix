"""Initial database schema

Revision ID: cf032c49b882
Revises:
Create Date: 2025-08-12 03:59:51.191084

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "cf032c49b882"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("application_date", sa.DateTime(), nullable=False),
        sa.Column("approval_date", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("home_directory", sa.String(), nullable=True),
        sa.Column("shell", sa.String(), nullable=False),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    # Create resource_limits table
    op.create_table(
        "resource_limits",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("disk_quota_mb", sa.Integer(), nullable=False),
        sa.Column("max_processes", sa.Integer(), nullable=False),
        sa.Column("cpu_limit_percent", sa.Integer(), nullable=False),
        sa.Column("memory_limit_mb", sa.Integer(), nullable=False),
        sa.Column("max_login_sessions", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_resource_limits_user_id"), "resource_limits", ["user_id"], unique=False
    )

    # Create applications table
    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("username_requested", sa.String(length=32), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("motivation", sa.String(), nullable=True),
        sa.Column("community_guidelines_accepted", sa.Boolean(), nullable=False),
        sa.Column("application_date", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("reviewed_by", sa.String(), nullable=True),
        sa.Column("review_date", sa.DateTime(), nullable=True),
        sa.Column("review_notes", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_applications_email"), "applications", ["email"], unique=False
    )

    # Create system_metrics table
    op.create_table(
        "system_metrics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("total_users", sa.Integer(), nullable=False),
        sa.Column("active_users_24h", sa.Integer(), nullable=False),
        sa.Column("cpu_usage_percent", sa.Float(), nullable=False),
        sa.Column("memory_usage_percent", sa.Float(), nullable=False),
        sa.Column("disk_usage_percent", sa.Float(), nullable=False),
        sa.Column("network_connections", sa.Integer(), nullable=False),
        sa.Column("ssh_sessions", sa.Integer(), nullable=False),
        sa.Column("web_requests_per_hour", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_system_metrics_timestamp"),
        "system_metrics",
        ["timestamp"],
        unique=False,
    )

    # Create user_metrics table
    op.create_table(
        "user_metrics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("cpu_time_seconds", sa.Integer(), nullable=False),
        sa.Column("memory_usage_mb", sa.Integer(), nullable=False),
        sa.Column("disk_usage_mb", sa.Integer(), nullable=False),
        sa.Column("active_processes", sa.Integer(), nullable=False),
        sa.Column("login_sessions", sa.Integer(), nullable=False),
        sa.Column("last_activity", sa.DateTime(), nullable=True),
        sa.Column("web_requests_count", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_user_metrics_timestamp"), "user_metrics", ["timestamp"], unique=False
    )
    op.create_index(
        op.f("ix_user_metrics_username"), "user_metrics", ["username"], unique=False
    )


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f("ix_user_metrics_username"), table_name="user_metrics")
    op.drop_index(op.f("ix_user_metrics_timestamp"), table_name="user_metrics")
    op.drop_table("user_metrics")

    op.drop_index(op.f("ix_system_metrics_timestamp"), table_name="system_metrics")
    op.drop_table("system_metrics")

    op.drop_index(op.f("ix_applications_email"), table_name="applications")
    op.drop_table("applications")

    op.drop_index(op.f("ix_resource_limits_user_id"), table_name="resource_limits")
    op.drop_table("resource_limits")

    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
