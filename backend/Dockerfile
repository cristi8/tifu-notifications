FROM python:3

RUN pip install cherrypy firebase-admin Pillow

COPY src /app
WORKDIR /app

STOPSIGNAL SIGINT
CMD ["python", "-u", "run.py"]
