FROM python:3

COPY ./app /app
RUN pip install --upgrade pip
WORKDIR /app
RUN pip3 install -r requirements.txt

#RUN python3 main.py

CMD ["./run.sh"]
