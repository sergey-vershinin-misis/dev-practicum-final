FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./img /code/img
COPY ./scenarios /code/scenarios
COPY ./service_adapters /code/service_adapters
COPY ./*.py /code/


CMD ["python", "main.py"]