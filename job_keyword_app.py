import src.message.consumer
from src.logger.logger import log

ENV = "dev"

if __name__ == '__main__':
    log.info(f"app starting")
    src.message.consumer.start_messaging()
