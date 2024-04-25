FROM python:3.10

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
COPY dir/src/main.py /usr/src/app
RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]
