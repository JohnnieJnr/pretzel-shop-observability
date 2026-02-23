FROM grafana/tempo:latest

# Use root to set up writable paths, then drop back to the image user (10001)
USER root

# Provide config at the standard path
COPY config.yml /etc/tempo.yaml

# Ensure trace storage paths exist; make them world-writable (rootless build cannot chown)
RUN mkdir -p \
      /var/tempo/metrics-generator \
      /var/tempo/metrics-generator-traces \
      /var/tempo/traces \
      /var/tempo/wal \
    && chmod -R 777 /var/tempo

# Drop back to the default non-root user from the base image
USER 10001

# Start Tempo with the explicit config file
ENTRYPOINT ["/tempo", "-config.file=/etc/tempo.yaml"]
