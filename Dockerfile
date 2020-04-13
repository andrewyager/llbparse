FROM python:3.7
RUN pip install requests beautifulsoup4
WORKDIR /opt/src
CMD python llbscrape.py