FROM python:slim

WORKDIR /usr/src/app

COPY app.py app.py
COPY score score
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install p5py PEP517
RUN pip install flask 
RUN pip install -r requirements.txt

CMD ["python", "app.py"]

