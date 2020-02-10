FROM python:3

COPY req.txt /req.txt
RUN pip install -r /req.txt

COPY . /app

WORKDIR /app

CMD ["python", "-u", "main.py"]
