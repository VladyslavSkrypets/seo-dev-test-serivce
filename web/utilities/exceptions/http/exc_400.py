from flask import make_response, jsonify, Response


def http_exc_400_payload_validation_error() -> Response:
    return make_response(jsonify("An error occurred while validating the request body."), 400)
