from datetime import datetime

from flask_restful import Resource


class HealthCheck(Resource):
    @staticmethod
    def get():
        return {"status": "alive", "datetime": str(datetime.utcnow())}
