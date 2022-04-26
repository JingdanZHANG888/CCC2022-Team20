
# Location: Melbourne
#
FROM python:3

COPY requirements.txt requirements.txt
USER myuser

# Install dependencies
RUN pip3 install --user -r requirements.txt

CMD ["python3", "./twitter_harvest.py"]
