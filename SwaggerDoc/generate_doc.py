from openapi_schema_pydantic.v3.v3_0_3 import OpenAPI
from openapi_schema_pydantic.v3.v3_0_3.util import construct_open_api_with_schema_class
from swagger_ui import api_doc

from SwaggerDoc.swaggerApiSchema import HANDWRITTEN_METHODS_MAP


def generate_open_api_json(paths: dict) -> str:
    obj = {
        "info": {"title": 'WebStudioApi', "version": "1.0"},
        "paths": {},
    }
    obj['paths'] |= paths
    return construct_open_api_with_schema_class(OpenAPI.parse_obj(obj)).json(by_alias=True, exclude_none=True, indent=2)


def fill_open_api_paths():
    text = {}
    for api_name in HANDWRITTEN_METHODS_MAP:
        text |= HANDWRITTEN_METHODS_MAP[api_name]
    return text


def generate_dock(app):
    api_doc(app, config_spec=generate_open_api_json(fill_open_api_paths()), url_prefix='/api/doc/v1', title='API doc')
