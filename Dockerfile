FROM python:3.6.2-alpine3.6

WORKDIR /cloudformation
RUN pip install awscli==1.15.2

ENTRYPOINT ["aws"]
CMD ["--version"]
