FROM python:3.13-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    lsb-release wget gnupg curl unzip expect ca-certificates locales \
    && sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen ru_RU.UTF-8

ENV LANG=ru_RU.UTF-8 \
    LANGUAGE=ru_RU:ru \
    LC_ALL=ru_RU.UTF-8

WORKDIR /YellowElephant

COPY requirements.txt .

RUN python3 -m venv .venv && \
    .venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /tmp/platform1c && \
    chmod +x ./onec/wget_1c.sh ./onec/setup_1c.exp

RUN --mount=type=secret,id=username \
    --mount=type=secret,id=pass \
    --mount=type=secret,id=1C_version \
    ./onec/wget_1c.sh && \
    ./onec/setup_1c.exp && \
    rm -rf /tmp/* ./installAsRoot ./*.run ./Liberica*.pdf ./Liberica*.txt ./readme.htm


FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    curl gnupg ca-certificates lsb-release locales \
    && sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
    && curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg \
    && apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client-16 \
    && sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen ru_RU.UTF-8 \
    && apt-get purge -y --auto-remove curl gnupg lsb-release \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=ru_RU.UTF-8 \
    LANGUAGE=ru_RU:ru \
    LC_ALL=ru_RU.UTF-8 \
    PATH="/YellowElephant/.venv/bin:$PATH"


COPY --from=builder /YellowElephant /YellowElephant
COPY --from=builder /opt/1cv8 /opt/1cv8

WORKDIR /YellowElephant

RUN groupadd -r db_manager && useradd -r -g db_manager -m -s /bin/bash db_manager \
    && chown -R db_manager:db_manager /YellowElephant

USER db_manager

CMD ["python", "main.py"]