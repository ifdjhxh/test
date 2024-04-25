FROM python:3.10

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app


COPY dir/src /usr/src/app

CMD [ "python", "main.py" ]
