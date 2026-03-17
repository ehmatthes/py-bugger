FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000"]

EXPOSE 8000