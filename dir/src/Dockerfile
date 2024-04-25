FROM python:3.10

RUN mkdir -p dir/src
WORKDIR dir/src

COPY . dir/src
RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]
