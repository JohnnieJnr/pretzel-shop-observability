FROM grafana/loki:latest

# Provide explicit config file location for the Loki process
COPY config.yml /etc/loki/config.yaml

# Start Loki with the provided config
ENTRYPOINT ["/usr/bin/loki", "-config.file=/etc/loki/config.yaml"]
