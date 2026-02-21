FROM otel/opentelemetry-collector-contrib:latest

WORKDIR /app

COPY config.yml /app/config.yml

CMD ["--config", "/app/config.yml"]