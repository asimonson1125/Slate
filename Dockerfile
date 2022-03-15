FROM python:3.9.8-bullseye
LABEL maintainer="Andrew Simonson <asimonson1125@gmail.com>"

WORKDIR /app
ADD ./src /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP="application.py"

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]