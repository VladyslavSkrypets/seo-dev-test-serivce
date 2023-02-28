import os
import logging
from datetime import datetime


_LOG_FOLDER = "logs"
_LOG_FOLDER_PATH = os.path.dirname(os.path.dirname(__file__))


if _LOG_FOLDER not in os.listdir(_LOG_FOLDER_PATH):
    os.mkdir(os.path.join(_LOG_FOLDER_PATH, _LOG_FOLDER))

logging.basicConfig(
    filename=os.path.join(
        _LOG_FOLDER_PATH, _LOG_FOLDER, f'{datetime.today().date()}.txt'
    ),
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s\t:  %(message)s',
    datefmt='%d.%m.%Y-%H:%M:%S'
)
