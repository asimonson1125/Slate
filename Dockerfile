FROM docker.io/python:3.8-buster
LABEL maintainer="Andrew Simonson <asimonson1125@gmail.com>"

WORKDIR /app
ADD ./src /app
COPY ./requirements.txt requirements.txt
RUN apt-get -yq install libsasl2-dev libldap2-dev libssl-dev gcc g++ make && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP="application.py"

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]