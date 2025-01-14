from alembic_utils.pg_extension import PGExtension

from services.data.models.fund import Fund
from services.data.models.round import Round

ltree_extension = PGExtension(
    schema="public",
    signature="ltree",
)


__all__ = ["Fund", "Round"]
