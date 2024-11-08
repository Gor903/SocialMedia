"""Follows

Revision ID: 5257acfdbbb1
Revises: e0e1e2669314
Create Date: 2024-11-04 02:24:29.383180

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "5257acfdbbb1"
down_revision: Union[str, None] = "e0e1e2669314"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_passwordreset_id", table_name="passwordreset")
    op.drop_table("passwordreset")
    op.drop_table("bp")
    op.drop_index("ix_profiles_id", table_name="profiles")
    op.drop_index("ix_profiles_username", table_name="profiles")
    op.drop_table("profiles")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("hashed_password", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("email_verified", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("refresh_token", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table(
        "profiles",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("username", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("surname", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("bio", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "social_links",
            postgresql.ARRAY(sa.VARCHAR()),
            autoincrement=False,
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name="profiles_pkey"),
    )
    op.create_index("ix_profiles_username", "profiles", ["username"], unique=True)
    op.create_index("ix_profiles_id", "profiles", ["id"], unique=False)
    op.create_table(
        "bp",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "username", sa.VARCHAR(length=100), autoincrement=False, nullable=False
        ),
        sa.Column("name", sa.VARCHAR(length=100), autoincrement=False, nullable=False),
        sa.Column(
            "surname", sa.VARCHAR(length=100), autoincrement=False, nullable=False
        ),
        sa.Column("bio", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column(
            "social_links",
            postgresql.ARRAY(sa.VARCHAR(length=100)),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="bp_pkey"),
    )
    op.create_table(
        "passwordreset",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("otp", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "expires_date",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("used", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="passwordreset_pkey"),
    )
    op.create_index("ix_passwordreset_id", "passwordreset", ["id"], unique=False)
    # ### end Alembic commands ###
