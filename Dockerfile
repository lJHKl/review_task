FROM python:3.10.0-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /
CMD ["uvicorn", "auth_part:app", "--port", "80"]
CMD ["uvicorn", "file_converter:app", "--port", "81"]
CMD ["uvicorn", "file_part:app", "--port", "82"]
