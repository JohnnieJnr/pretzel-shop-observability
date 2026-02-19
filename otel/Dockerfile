FROM otel/opentelemetry-collector-contrib:latest

COPY --chown=10001:10001 config.yml /etc/otelcol/config.yaml

USER 10001

ENTRYPOINT ["/otelcontribcol"]
CMD ["--config=/etc/otelcol/config.yaml"]
