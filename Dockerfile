FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY baselinewebapp/requirements.txt /

WORKDIR /

RUN pip install -r ./requirements.txt --no-cache-dir

COPY baselinewebapp/ /app/

WORKDIR /app

ENV FLASK_APP=app.py
CMD flask db upgrade && flask run -h 0.0.0.0 -p 5000
