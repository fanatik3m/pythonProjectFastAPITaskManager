FROM python:3.9

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install python-dotenv

COPY . .

RUN chmod a+x docker/app.sh