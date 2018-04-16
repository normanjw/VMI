import logging
import json
import os
import re
from jsonschema import Draft4Validator

class SchemaValidator(object):
    json_validator = None
    logger = logging.getLogger(__name__)

    @classmethod
    def initialize(cls):
        cls.logger.warning("Initializing JSON validator for the defined schema.")
        path = os.path.join(os.path.dirname(__file__), 'item_inventory_schema.json')
        with open(path, 'r') as json_file:
            schema_json = json.load(json_file)
        cls.json_validator = Draft4Validator(schema_json)

    @classmethod
    def validate(cls, input_json):
        validation_errors = {}
        errors = cls.json_validator.iter_errors(input_json)
        for error in sorted(errors, key=str):
            msg = error.message
            if len(error.path) > 0:
                fld_name = '.'.join([str(i) for i in error.path])
            else:
                fld_name = re.split('\W+', msg)[1]
            if fld_name not in validation_errors:
                validation_errors[fld_name] = [msg]
            else:
                validation_errors[fld_name].append(msg)
        return validation_errors

