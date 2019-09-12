FROM python:3.6-slim

RUN apt-get update -y \
    && apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev libsnmp-dev -y

RUN pip install flask && pip install requests

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./src/ .

EXPOSE 8080

ENTRYPOINT ["python"]
CMD ["timeline.py"]