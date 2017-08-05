FROM python:3.6.2-alpine3.6

WORKDIR /test2
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ecs.yml .

ENV AWS_DEFAULT_REGION=us-west-2

ENTRYPOINT ["aws"]
CMD ["--version"]
