from multiprocessing import Process

from job_keyword_app import start_test_server
from message.consumer import start_messaging


def start_web():
    start_test_server()


def start_app():
    messaging_process = Process(target=start_messaging)
    web_process = Process(target=start_web)
    messaging_process.start()
    web_process.start()


if __name__ == '__main__':
    start_app()