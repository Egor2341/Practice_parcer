FROM python:3.11

RUN mkdir /Frontend

WORKDIR /Frontend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn front:front_app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000



