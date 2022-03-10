FROM python:3.9.8-bullseye
LABEL maintainer="Andrew Simonson <asimonson1125@gmail.com>"

WORKDIR /app/
COPY ./requirements.txt /app/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./website /app/
COPY ./.git /app/

run python -m flask db upgrade; exit 0

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]