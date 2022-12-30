FROM tiangolo/uwsgi-nginx-flask
WORKDIR /app
COPY . .
EXPOSE 5000
ENV FLASK_APP=search.py
CMD ["flask", "run", "--host", "0.0.0.0"]