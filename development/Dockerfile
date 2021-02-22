
ARG python_ver=3.7
FROM python:${python_ver}

ARG nautobot_ver=v1.0.0b1
ENV PYTHONUNBUFFERED 1

RUN mkdir /prom_cache
ENV prometheus_multiproc_dir /prom_cache

RUN mkdir -p /opt/nautobot

RUN pip install --upgrade pip\
  && pip install poetry

# -------------------------------------------------------------------------------------
# Install Nautobot
# -------------------------------------------------------------------------------------
COPY packages/nautobot-1.0.0b1-py3-none-any.whl /tmp
RUN pip install /tmp/nautobot-1.0.0b1-py3-none-any.whl

# -------------------------------------------------------------------------------------
# Install Nautobot Plugin
# -------------------------------------------------------------------------------------
RUN mkdir -p /source
WORKDIR /source
COPY . /source
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

ENV NAUTOBOT_CONFIG /opt/nautobot/configuration.py
WORKDIR /opt/nautobot/
