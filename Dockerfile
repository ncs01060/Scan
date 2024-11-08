FROM python:3.11.0
WORKDIR /LG
COPY . /LG

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python","scan.py" ]