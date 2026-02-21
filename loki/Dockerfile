FROM grafana/loki:2.9.4

COPY config.yml .

ENTRYPOINT ["/usr/bin/loki", "./config.yaml"]
