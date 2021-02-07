import os
import pathlib
import platform
import sys
from pathlib import Path

import src.message.consumer
from src.logger.logger import log

ENV = "dev"


def init_logging() -> None:
    log.info(f"** Your starting script path is {pathlib.Path(__file__).parent.absolute()}")
    log.info(f"** Your OS name is: {os.name}, {platform.system()}, {platform.release()}")
    log.info(f"** The version of Python you are running is: {platform.python_version()}")
    log.info(f"** Your user home directory is: {Path.home()}")
    log.info(f"** Your Python installation directory is: {sys.executable}")
    log.info(f"** Amount of Your CPU cores: {os.cpu_count()}")


if __name__ == '__main__':
    log.info(f"app starting")
    init_logging()
    src.message.consumer.start_messaging()
