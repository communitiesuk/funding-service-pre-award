from jsonschema import validate

from assessment_store.config.mappings.assessment_mapping_schema import (
    top_level_assessment_mapping_schema as schema,
)
from config import Config


def test_assessment_mapping_conforms_to_schema():
    for _key, value in Config.ASSESSMENT_MAPPING_CONFIG.items():
        assert validate(instance=value, schema=schema) is None