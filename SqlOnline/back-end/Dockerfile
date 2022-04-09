FROM python:3.9

MAINTAINER @amigo2208
# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . /code/

# Generate keys 
RUN ssh-keygen -t rsa -b 4096 -m PEM -f jwtRS256.key -q -P "" && openssl rsa -in jwtRS256.key -pubout -outform PEM -out jwtRS256.key.pub
#RUN python key_gen.py

# 
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
 
