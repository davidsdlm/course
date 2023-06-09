FROM python:3.10

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

#CMD [ "python3", "app.py"]
ENTRYPOINT gunicorn app:app --workers 1 --threads 1 -b 0.0.0.0:5000