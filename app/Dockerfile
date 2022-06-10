FROM python:3.7.9-slim-stretch

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install --upgrade pip -r requirements.txt


COPY main.py /app
COPY models.py /app
COPY settings.py /app
ADD data /app/data
ADD templates /app/templates

# Устанавливаем порт, который будет использоваться для сервера
#EXPOSE 80