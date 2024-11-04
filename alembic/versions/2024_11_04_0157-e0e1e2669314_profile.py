"""Profile

Revision ID: e0e1e2669314
Revises: 
Create Date: 2024-11-04 01:57:55.271327

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "e0e1e2669314"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_passwordreset_id", table_name="passwordreset")
    op.drop_table("passwordreset")
    op.drop_table("bp")
    op.drop_index("ix_accounts_id", table_name="accounts")
    op.drop_index("ix_accounts_username", table_name="accounts")
    op.drop_table("accounts")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
    op.drop_table("follows")
    op.drop_index("ix_profiles_id", table_name="profiles")
    op.drop_index("ix_profiles_username", table_name="profiles")
    op.drop_table("profiles")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
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
        "follows",
        sa.Column("follower_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("followee_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "followed_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["followee_id"], ["accounts.id"], name="follows_followee_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["follower_id"], ["accounts.id"], name="follows_follower_id_fkey"
        ),
        sa.PrimaryKeyConstraint("follower_id", "followee_id", name="follows_pkey"),
    )
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
        "accounts",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("username", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="accounts_pkey"),
    )
    op.create_index("ix_accounts_username", "accounts", ["username"], unique=True)
    op.create_index("ix_accounts_id", "accounts", ["id"], unique=False)
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
