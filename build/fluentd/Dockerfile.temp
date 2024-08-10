FROM fluent/fluentd:edge

USER root

RUN fluent-gem install fluent-plugin-elasticsearch

COPY build/fluentd/fluent.conf /fluentd/etc/fluent.conf

RUN mkdir -p /var/log/td-agent && \
    chown -R fluent:fluent /var/log/td-agent

USER fluent

EXPOSE 5141 5141/udp 5142 5142/udp 24224 24224/udp 9880

CMD ["fluentd", "-c", "/fluentd/etc/fluent.conf"]
