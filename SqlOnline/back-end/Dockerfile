MAINTAINER @amigo2208

# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . /code/

# Generate keys 
RUN rm jwtRS256.key > /dev/null 2>&1 && rm jwtRS256.key.pub > /dev/null 2>&1
RUN ssh-keygen -t rsa -b 4096 -m PEM -f jwtRS256.key -q -P "" && openssl rsa -in jwtRS256.key -pubout -outform PEM -out jwtRS256.key.pub
#RUN python key_gen.py

# 
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
 
