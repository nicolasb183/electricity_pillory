FROM python:latest
WORKDIR /usr/local/bin
COPY getUser.py requirements.txt  ./
ADD templates /usr/local/bin/templates
#RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
CMD  python3 getUser.py --host=0.0.0.0
ENV PORT 5000
EXPOSE 5000

