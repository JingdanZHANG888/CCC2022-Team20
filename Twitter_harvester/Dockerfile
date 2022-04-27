
# Location: Melbourne
#
FROM python:3

COPY requirements.txt requirements.txt
COPY keywords.json keywords.json
COPY twitter_harvest.py twitter_harvest.py
COPY twitter_keys.json twitter_keys.json 

# ADD twitter_harvest.py /
# Install dependencies
RUN pip3 install --user -r requirements.txt

CMD ["python3", "/twitter_harvest.py"]
