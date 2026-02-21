FROM otel/opentelemetry-collector-contrib:latest

WORKDIR /app

COPY config.yml .

CMD ["--config", "/app/config.yml"]