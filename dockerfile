FROM python:3.10

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN chmod +x run.sh

#CMD [ "python3", "app.py"]
ENTRYPOINT ["./run.sh"]