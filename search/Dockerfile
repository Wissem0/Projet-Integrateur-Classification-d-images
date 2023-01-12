FROM python:3.9-slim-buster
WORKDIR /app
COPY . .
RUN pip install -r ./flask_service/requirements.txt
EXPOSE 5000
# ENV FLASK_APP=flask_service/app.py
# ENV PATH=$PATH:/flask_service
# ENV PYTHONPATH /flask_service
WORKDIR /app/flask_service

CMD python ./app.py
