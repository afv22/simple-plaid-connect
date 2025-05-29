FROM python:alpine

WORKDIR /server

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "-u", "server.py"]