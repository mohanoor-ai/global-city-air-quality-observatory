FROM apache/airflow:3.1.8

USER root

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
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    && rm -rf /var/lib/apt/lists/*

USER airflow

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt
