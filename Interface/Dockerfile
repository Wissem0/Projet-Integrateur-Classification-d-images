FROM tiangolo/uwsgi-nginx-flask
WORKDIR /app
COPY . .
RUN pip install -r ./requirements.txt
EXPOSE 3141
ENV FLASK_APP=interface.py
CMD python interface.py
