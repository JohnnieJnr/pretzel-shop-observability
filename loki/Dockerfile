FROM grafana/loki:latest

COPY config.yml .

ENTRYPOINT ["/usr/bin/loki", "./config.yaml"]
