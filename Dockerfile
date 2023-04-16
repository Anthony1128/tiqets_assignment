FROM python:3.9-slim-buster

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app
WORKDIR /app
CMD ["python", "main.py"]