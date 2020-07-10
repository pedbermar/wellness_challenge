FROM python:3.7 

COPY . /opt/wellness_challenge

RUN apt-get update
RUN apt-get install -y virtualenv python-pip


WORKDIR /opt/wellness_challenge/
RUN pip install -r requirements.txt
RUN  python setup.py develop

CMD ["pserve", "--reload", "development.ini"]