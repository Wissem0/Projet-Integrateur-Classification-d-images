FROM tensorflow/tensorflow
WORKDIR /app
COPY . .
RUN pip install -r ./requirements.txt
# RUN python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-0.12.0-py3-none-any.whl
EXPOSE 8083
# ENV FLASK_APP=flaskService.py
CMD python test.py
