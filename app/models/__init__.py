# Import every model here so Base.metadata knows about all tables (Alembic reads it).
from app.models.user import User  # noqa: F401
