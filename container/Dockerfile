# Multi-Stage Container Image for QENTA-PRIME UAO Master Build
FROM mcr.microsoft.com/powershell:nanoserver-ltsc2022 AS base
WORKDIR /app

# Install Python & Core Modules
ENV PYTHONUNBUFFERED=1
ENV ZERO_COST_LOCK=1

COPY . /app/living_repository

EXPOSE 8088 8443 8094 8095 8099 50050

CMD ["pwsh", "-Command", "python /app/living_repository/bin/launch_iis_https_web_app.py"]
