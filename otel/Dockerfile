FROM otel/opentelemetry-collector:latest

WORKDIR /app

COPY config.yml ./config.yml

CMD ["--config", "/app/config.yml"]