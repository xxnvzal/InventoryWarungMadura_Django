FROM python:latest
WORKDIR /code
COPY code/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1
CMD ["sleep", "infinity"]