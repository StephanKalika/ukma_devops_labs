# Monitoring Stack with Prometheus, Loki, and Grafana

This repository contains a Docker Compose setup for monitoring a laptop or server using:

- Prometheus for metrics collection
- Node Exporter for system metrics
- Loki for log aggregation
- Promtail for log shipping
- Grafana for visualization

## Setup Instructions

1. Clone this repository:
git clone https://github.com/StephanKalika/ukma_devops_labs.git cd monitoring

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

### Key Metrics at a Glance
- CPU usage monitoring with threshold indicators
- Memory usage percentage with visual indicators
- Disk usage percentage with visual indicators
- CPU cores count

### Detailed Resource Monitoring
- Detailed CPU usage breakdown (system, user, IO wait)
- Memory usage details (total, used, cached, free)
- Disk space allocation and usage
- Network traffic monitoring (receive and transmit)

### System Information
- System load averages (1m, 5m, 15m)
- System uptime tracking
- Network interfaces and filesystems count

### Logs Visualization
- System logs visualization with filtering capabilities