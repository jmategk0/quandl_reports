FROM python:3.6.11-buster

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

CMD ["python", "./hello.py"]