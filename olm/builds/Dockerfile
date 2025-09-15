FROM container-registry.oracle.com/os/oraclelinux:8
COPY rpms /tmp/
RUN dnf install -y /tmp/*.rpm &&\
    dnf clean all &&\
    rm -rf /var/cache/yum/* /tmp/*.rpm

FROM container-registry.oracle.com/os/oraclelinux:8-slim

COPY --from=0 /usr/share/licenses/node-exporter-container-bin /usr/share/licenses/node-exporter
# Our entrypoint is intentionally bin/node_exporter to mimic the upstream repo used by Prometheus
COPY --from=0 /usr/bin/node-exporter /usr/bin/node_exporter
RUN microdnf clean all &&\
    rm -rf /var/cache/yum/* &&\
    test -d /LICENSES || ln -s /usr/share/licenses /LICENSES

EXPOSE 9100

USER nobody

ENTRYPOINT  [ "/usr/bin/node_exporter"]
