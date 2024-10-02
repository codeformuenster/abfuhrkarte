FROM ghcr.io/astral-sh/uv:0.4.18-bookworm

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales && \
  rm -rf /var/lib/apt/lists/* && \
  sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && \
  dpkg-reconfigure --frontend=noninteractive locales && \
  update-locale LANG=de_DE.UTF-8

ENV LANG=de_DE.UTF-8 LC_ALL=de_DE.UTF-8

USER 1000

COPY --chown=1000:1000 . /app

WORKDIR /app

RUN uv sync --frozen

ENTRYPOINT ["uv", "run", "abfuhrkarte.py"]
