from flask import Flask

app = Flask(__name__)

from .keyword_controller import post_job_keywords, get_job_keywords

