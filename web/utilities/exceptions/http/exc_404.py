from flask import make_response, jsonify, Response


def http_exc_404_payload_validation_error() -> Response:
    return make_response(jsonify("This resource does not exist."), 404)
