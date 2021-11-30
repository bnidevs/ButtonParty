import json
import jsonschema
from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "streak": {"type": "number"}
    }
}

def validateJson(jsonData):
    try:
        validate(instance=jsonData, schema=schema)
    except Exception as err:
        return False
    return True
