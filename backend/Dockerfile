FROM python:3.11.0

WORKDIR /backend

COPY . ./

RUN pip install -r requirements-flask.txt

RUN pip install -r requirements-scrapy.txt

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "-t","900","app:app"]