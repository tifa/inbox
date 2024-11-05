FROM python:3.12 AS web

ENV PYTHONPATH=/app \
    UV_SYSTEM_PYTHON=true

COPY ./inbox/.bashrc /root/.bashrc
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install uv && uv pip install -r /app/requirements.txt

COPY ./ /app


ENTRYPOINT ["/app/inbox/app.py"]



FROM ubuntu:22.04 AS server

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONPATH=/app \
    UV_SYSTEM_PYTHON=true

RUN apt-get update \
    && apt-get install software-properties-common -y --no-install-recommends \
    && add-apt-repository universe -y \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        ansible \
        gcc \
        make \
        libonig-dev \
        python3-dev \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY ./ /app
COPY ./inbox/.bashrc /root/.bashrc

WORKDIR /app

RUN pip3 install -U uv

CMD ["tail", "-f", "/dev/null"]


# # Install packages
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#         ca-certificates \
#         curl \
#         gnupg \
#     # Ansible
#     && apt-get update \
#     && apt-get install -y --no-install-recommends \
#         ansible \
#         apache2 \
#         certbot \
#         cron \
#         dnsutils \
#         dovecot-lmtpd \
#         dovecot-sqlite \
#         fail2ban \
#         gcc \
#         less \
#         libdb-dev \
#         libsqlite3-dev \
#         m4 \
#         mailutils \
#         make \
#         opendkim \
#         opendkim-tools \
#         pflogsumm \
#         postfix-policyd-spf-python \
#         postfix-sqlite \
#         python3-certbot-apache \
#         rsyslog \
#         sqlite3 \
#         sshpass \
#     && rm -rf /var/lib/apt/lists/* \
#     && apt-get autoremove -y
