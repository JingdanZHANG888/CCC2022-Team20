
# Location: Melbourne
#
FROM python:3

ADD . /

# Install dependencies
RUN pip3 install --user -r requirement.txt

CMD ["python3", "/Twitter_Aurin_analysis.py"]
