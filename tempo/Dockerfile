FROM grafana/tempo:latest

# Provide config at the standard path
COPY config.yml /etc/tempo.yaml

# Start Tempo with the explicit config file
ENTRYPOINT ["/tempo", "-config.file=/etc/tempo.yaml"]
