FROM otel/opentelemetry-collector-contrib:0.146.0

WORKDIR /app

COPY config.yml /app/config.yml

CMD ["--config", "/app/config.yml"]