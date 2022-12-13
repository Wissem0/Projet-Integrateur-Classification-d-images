FROM tiangolo/uwsgi-nginx-flask
WORKDIR /app
COPY . .
EXPOSE 8080
ENV FLASK_APP=search.py
CMD python flask_service/search.py 
