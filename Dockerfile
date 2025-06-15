FROM apache/airflow:3.0.2

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
            curl \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Install uv
RUN curl -Ls https://astral.sh/uv/install.sh | bash

# Ensure uv is in PATH
ENV PATH="/root/.cargo/bin:$PATH"

USER airflow

# Install dependencies
COPY pyproject.toml /tmp/pyproject.toml
RUN uv pip install -r /tmp/pyproject.toml