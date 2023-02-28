from flask_restful import Resource
from flask import request, jsonify, make_response
from pydantic.error_wrappers import ValidationError

from web.utilities.logger import logging
from web.schemas.domain_statistic import DomainStatisticPayload
from web.api.services.domain_statistic import DomainStatisticInfo
from web.utilities.exceptions.http.exc_400 import http_exc_400_payload_validation_error


class DomainStatistic(Resource):
    @staticmethod
    def post():
        try:
            payload = DomainStatisticPayload(**request.get_json(force=True))
        except ValidationError:
            logging.error((
                f"Validation error during processing user request payload"
                f"\nPayload: \n{request.get_json(force=True)}"
                f"\nPath: \n{request.url}"
            ), exc_info=True)
            return http_exc_400_payload_validation_error()

        domain_statistic_info = (
            DomainStatisticInfo()
            .gather(domain_name=payload.domain_name, search_depth=2)
            .dict()
        )

        return make_response(jsonify(domain_statistic_info), 200)
