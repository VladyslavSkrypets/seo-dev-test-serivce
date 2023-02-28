from waitress import serve
from flask_restful import Api
from flask import Flask, request

from web.config.manager import settings
from web.utilities.logger import logging
from web.api.resources.health_check import HealthCheck
from web.config.settings.environment import Environment
from web.api.resources.domain_statistic import DomainStatistic
from web.api.resources.page_view_registration import PageViewRegistration
from web.utilities.exceptions.http.exc_404 import http_exc_404_payload_validation_error


app = Flask(__name__)
api = Api(app)


@app.errorhandler(404)
def resource_not_found_error(e):
    logging.error((
        f"The requested resource was not found."
        f"\nURL: {request.url}"
    ), exc_info=True)
    return http_exc_404_payload_validation_error()


api.add_resource(HealthCheck, '/', endpoint='root')
api.add_resource(HealthCheck, '/healthcheck', endpoint='healthcheck')
api.add_resource(DomainStatistic, f"{settings.API_PREFIX}/domain-statistic")
api.add_resource(PageViewRegistration, f"{settings.API_PREFIX}/page-view-registration")


def app_runner() -> None:
    if settings.ENVIRONMENT == Environment.DEVELOPMENT:
        logging.info("Run app in development mode")
        app.run(
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
            use_reloader=settings.RELOAD,
            processes=settings.SERVER_WORKERS,
            debug=settings.DEBUG
        )
    else:
        logging.info("Run app in production mode")
        serve(
            app=app,
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT
        )


if __name__ == '__main__':
    app_runner()
