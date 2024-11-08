FROM python:latest

RUN pip install pyairvisual prometheus_client

ADD main.py main.py

CMD ["python","-u", "main.py"]