FROM python:3.7.8
WORKDIR /project
ADD . /project
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
CMD ["python", "job_keyword_app.py"]