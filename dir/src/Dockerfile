FROM python:3.10

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r dir/src/requirements.txt
COPY dir/src /usr/src/app

CMD [ "python", "main.py" ]
