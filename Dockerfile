FROM python:3.7 


RUN apt-get update
RUN apt-get install -y python-pip

WORKDIR /opt/wellness_challenge/

COPY . /opt/wellness_challenge
RUN  python setup.py develop

CMD ["pserve", "--reload", "development.ini"]

