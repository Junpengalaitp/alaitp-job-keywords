from multiprocessing import Process

from job_keyword_app import start_test_server
from message.consumer import start_messaging


def start_web():
    start_test_server()


if __name__ == '__main__':
    web_process = Process(target=start_web)
    web_process.start()
    start_messaging()