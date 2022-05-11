
# COMP90024 Assignment 2 Team 20
# Cenxi Si 1052447 located in China
# Yipei Liu 1067990 located in China
# Jingdan Zhang 1054101 located in China
# Chengyan Dai 1054219 located in Melbourne
# Ruimin Sun 1052182 located in China
#
FROM python:3

ADD . /

# Install dependencies
RUN pip3 install --user -r requirements.txt

CMD ["python3", "/Twitter_Aurin_analysis.py"]
