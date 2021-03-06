FROM python:3.7.8-slim-buster
WORKDIR /project
ADD ./requirements.txt /project/requirements.txt
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
ADD . /project
ENTRYPOINT ["python", "job_keyword_app.py"]