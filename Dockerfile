FROM python:3.6

RUN apt-get update

COPY . /weather_fl0

WORKDIR /weather_fl0

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]