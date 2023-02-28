from flask_restful import Resource
from flask import request, jsonify, make_response
from pydantic.error_wrappers import ValidationError

from web.database.base import get_db
from web.utilities.logger import logging
from web.schemas.page_view_registration import PageViewRegistrationPayload
from web.utilities.exceptions.http.exc_400 import http_exc_400_payload_validation_error
from web.api.services.page_view_registration import PageViewRegistrationInfo, save_page_view_registration_info


class PageViewRegistration(Resource):
    @staticmethod
    def post():
        try:
            payload = PageViewRegistrationPayload(**request.get_json(force=True))
        except ValidationError:
            logging.error((
                f"Validation error during processing user request payload"
                f"\nPayload: \n{request.get_json(force=True)}"
                f"\nPath: \n{request.url}"
            ), exc_info=True)
            return http_exc_400_payload_validation_error

        page_view_registration_info = (
            PageViewRegistrationInfo()
            .gather(url=payload.url)
            .dict()
        )
        try:
            save_page_view_registration_info({
                'url_to_scan': str(payload.url),
                **page_view_registration_info
            })
        except Exception:
            logging.error("Error occurred during saving payload database", exc_info=True)

        return make_response(jsonify(page_view_registration_info), 200)
