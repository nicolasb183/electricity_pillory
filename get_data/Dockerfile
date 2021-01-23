FROM python:latest
WORKDIR /usr/local/bin
COPY requirements.txt  ./
#RUN /usr/local/bin/python -m pip install --upgrade pip
RUN  pip3 install --no-cache-dir -r requirements.txt
CMD  ["python3", "/usr/local/bin/scripts/getData.py"]

