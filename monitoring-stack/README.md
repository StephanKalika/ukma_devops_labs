# Monitoring Stack with Prometheus, Loki, and Grafana

This repository contains a Docker Compose setup for monitoring a laptop or server using:

- Prometheus for metrics collection
- Node Exporter for system metrics
- Loki for log aggregation
- Promtail for log shipping
- Grafana for visualization

## Setup Instructions

1. Clone this repository:
git clone https://github.com/StephanKalika/ukma_devops_labs.git cd monitoring-stack

2. Start the monitoring stack:
docker-compose up -d

3. Access Grafana:
- URL: http://localhost:3000
- Username: admin
- Password: admin

4. The dashboard "System Monitoring Dashboard" should be automatically loaded.

## Components

- Prometheus (http://localhost:9090): Metrics database
- Node Exporter (http://localhost:9100): System metrics collector
- Loki (http://localhost:3100): Log aggregation system
- Grafana (http://localhost:3000): Visualization platform

## Dashboard

The included dashboard provides:
- CPU usage monitoring
- Memory usage monitoring
- Disk usage monitoring
- Network traffic monitoring
- System logs visualization