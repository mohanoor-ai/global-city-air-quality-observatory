FROM apache/airflow:3.1.8

USER 0

RUN grep -q '^root:' /etc/passwd || echo 'root:x:0:0:root:/root:/bin/bash' >> /etc/passwd \
    && grep -q '^root:' /etc/group || echo 'root:x:0:' >> /etc/group \
    && grep -q '^_apt:' /etc/passwd || echo '_apt:x:100:65534::/nonexistent:/usr/sbin/nologin' >> /etc/passwd \
    && grep -q '^staff:' /etc/group || echo 'staff:x:50:' >> /etc/group \
    && grep -q '^sasl:' /etc/group || echo 'sasl:x:45:' >> /etc/group \
    && grep -q '^airflow:' /etc/passwd || echo 'airflow:x:50000:0:Airflow:/opt/airflow:/bin/bash' >> /etc/passwd

RUN rm -f \
        /etc/apt/sources.list.d/*docker* \
        /etc/apt/sources.list.d/*mariadb* \
        /etc/apt/sources.list.d/*microsoft* \
        /etc/apt/sources.list.d/*postgres* \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        openjdk-17-jre-headless \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg \
        | gpg --dearmor -o /etc/apt/keyrings/google-cloud-cli.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/google-cloud-cli.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
        > /etc/apt/sources.list.d/google-cloud-cli.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-cloud-cli \
    && rm -rf /var/lib/apt/lists/*

USER 50000

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir 'apache-airflow[celery,postgres]==3.1.8' \
    && pip install --no-cache-dir -r /tmp/requirements.txt
