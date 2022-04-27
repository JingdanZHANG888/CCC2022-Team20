
# Location: Melbourne
#
FROM python:3

#COPY requirements.txt requirements.txt

ADD . /
# Install dependencies
RUN pip3 install --user -r requirements.txt

CMD ["python3", "/twitter_harvest.py"]
