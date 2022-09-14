FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY dao dao
COPY service service
COPY tests tests
COPY views views
COPY app.py .
COPY implemented.py .
COPY decorator.py .
COPY setup_db.py .
COPY create_db.py .

CMD flask run -h 0.0.0.0 -p 80
