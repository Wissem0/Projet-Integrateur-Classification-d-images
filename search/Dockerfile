FROM tiangolo/uwsgi-nginx-flask
WORKDIR /app
COPY . .
RUN pip install -r ./flask_service/requirements.txt
EXPOSE 5000
ENV FLASK_APP=flask_service/app.py
CMD ["flask", "run", "--host", "0.0.0.0"]
