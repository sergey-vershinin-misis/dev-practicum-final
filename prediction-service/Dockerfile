FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Required to successfully install dependencies for geopandas library
RUN apt-get update
RUN apt-get install -y gdal-bin libgdal-dev g++

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
