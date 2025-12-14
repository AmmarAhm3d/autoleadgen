# Deployment Guide

Complete guide to deploying AutoLeadGen in various environments.

## 📋 Table of Contents

1. [Development Setup](#development-setup)
2. [Local Production](#local-production)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 Development Setup

### Prerequisites
- Python 3.10+
- Git
- Virtual environment support

### Installation

```bash
# Clone repository
git clone https://github.com/AmmarAhm3d/autoleadgen.git
cd autoleadgen

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Initialize database
python scripts/init_db.py

# Run tests
pytest

# Start development server
python -m autoleadgen.cli --debug
```

### Development Commands

```bash
# Run with debug logging
python -m autoleadgen.cli --debug --log-level DEBUG

# Run specific agent
python -m autoleadgen.cli --agent scraper --query "nursing home"

# Run with hot reload
watchmedo auto-restart -d src -p '*.py' -- python -m autoleadgen.cli
```

---

## 🚀 Local Production

### Prerequisites
- Python 3.10+ (production-grade)
- Nginx or Apache (reverse proxy)
- Supervisor or systemd (process management)
- PostgreSQL or SQLite with WAL mode

### Setup

#### 1. Install Production Dependencies

```bash
# Use production requirements
pip install -r requirements-prod.txt

# No development tools
pip uninstall -y pytest black flake8 mypy
```

#### 2. Create System User

```bash
# Create dedicated user
sudo useradd -r -s /bin/bash autoleadgen

# Create application directory
sudo mkdir -p /opt/autoleadgen
sudo chown autoleadgen:autoleadgen /opt/autoleadgen
```

#### 3. Deploy Application

```bash
# Copy files
sudo cp -r . /opt/autoleadgen/

# Set permissions
sudo chown -R autoleadgen:autoleadgen /opt/autoleadgen
sudo chmod 755 /opt/autoleadgen

# Create data directory
sudo mkdir -p /var/lib/autoleadgen
sudo chown autoleadgen:autoleadgen /var/lib/autoleadgen
sudo chmod 700 /var/lib/autoleadgen
```

#### 4. Configure Environment

```bash
# Copy and edit production .env
sudo cp /opt/autoleadgen/.env.example /var/lib/autoleadgen/.env
sudo chown autoleadgen:autoleadgen /var/lib/autoleadgen/.env
sudo chmod 600 /var/lib/autoleadgen/.env

# Add to file
sudo nano /var/lib/autoleadgen/.env

# Content:
# DATABASE_URL=sqlite:////var/lib/autoleadgen/leads.db
# LOG_FILE=/var/log/autoleadgen/app.log
# LOG_LEVEL=INFO
# DEBUG=False
```

#### 5. Setup Process Management (systemd)

```bash
# Create systemd service
sudo nano /etc/systemd/system/autoleadgen.service
```

```ini
[Unit]
Description=AutoLeadGen Service
After=network.target

[Service]
Type=simple
User=autoleadgen
Group=autoleadgen
WorkingDirectory=/opt/autoleadgen
Environment="PATH=/opt/autoleadgen/venv/bin"
EnvironmentFile=/var/lib/autoleadgen/.env
ExecStart=/opt/autoleadgen/venv/bin/python -m autoleadgen.cli
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable autoleadgen
sudo systemctl start autoleadgen

# Check status
sudo systemctl status autoleadgen

# View logs
sudo journalctl -u autoleadgen -f
```

#### 6. Configure Reverse Proxy (Nginx)

```nginx
# /etc/nginx/sites-available/autoleadgen
upstream autoleadgen {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://autoleadgen;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Logging
    access_log /var/log/nginx/autoleadgen.access.log;
    error_log /var/log/nginx/autoleadgen.error.log;
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/autoleadgen /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. SSL/TLS Setup

```bash
# Using Let's Encrypt
sudo apt install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --nginx -d api.example.com

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## 🐳 Docker Deployment

### Prerequisites
- Docker
- Docker Compose (optional)

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    chromium-browser \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-prod.txt

# Install Playwright browsers
RUN playwright install chromium

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "-m", "autoleadgen.cli"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  autoleadgen:
    build: .
    container_name: autoleadgen
    environment:
      - YELP_API_KEY=${YELP_API_KEY}
      - FIRECRAWL_API_KEY=${FIRECRAWL_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - DATABASE_URL=sqlite:////data/leads.db
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/data
      - ./logs:/app/logs
    ports:
      - "8000:8000"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:latest
    container_name: autoleadgen-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - autoleadgen
    restart: unless-stopped
```

### Build and Run

```bash
# Build image
docker build -t autoleadgen:latest .

# Run container
docker run -d \
  --name autoleadgen \
  -e YELP_API_KEY=$YELP_API_KEY \
  -e FIRECRAWL_API_KEY=$FIRECRAWL_API_KEY \
  -v $(pwd)/data:/data \
  -p 8000:8000 \
  autoleadgen:latest

# Using Docker Compose
docker-compose up -d

# Check logs
docker logs -f autoleadgen
```

---

## ☁️ Cloud Deployment

### AWS Deployment

#### Option 1: EC2 + RDS

```bash
# Create EC2 instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.medium \
  --key-name my-key \
  --security-groups autoleadgen-sg

# SSH into instance
ssh -i my-key.pem ec2-user@<instance-ip>

# Follow local production setup
```

#### Option 2: ECS + Fargate

```bash
# Create task definition
aws ecs register-task-definition \
  --family autoleadgen \
  --requires-compatibilities FARGATE \
  --network-mode awsvpc \
  --cpu 256 \
  --memory 512 \
  --container-definitions file://task-definition.json

# Create service
aws ecs create-service \
  --cluster default \
  --service-name autoleadgen \
  --task-definition autoleadgen \
  --desired-count 2
```

### Google Cloud Deployment

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/my-project/autoleadgen

# Deploy to Cloud Run
gcloud run deploy autoleadgen \
  --image gcr.io/my-project/autoleadgen \
  --platform managed \
  --region us-central1 \
  --set-env-vars YELP_API_KEY=$YELP_API_KEY,FIRECRAWL_API_KEY=$FIRECRAWL_API_KEY
```

### Azure Deployment

```bash
# Create resource group
az group create --name autoleadgen --location eastus

# Build container
az acr build --registry myacr --image autoleadgen:latest .

# Deploy to App Service
az webapp create --resource-group autoleadgen \
  --plan myplan --name autoleadgen
```

---

## 🚢 Kubernetes Deployment

### Prerequisites
- kubectl
- Kubernetes cluster (EKS, GKE, AKS, or local)

### Deployment Manifest

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: autoleadgen
spec:
  replicas: 3
  selector:
    matchLabels:
      app: autoleadgen
  template:
    metadata:
      labels:
        app: autoleadgen
    spec:
      containers:
      - name: autoleadgen
        image: autoleadgen:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
        env:
        - name: YELP_API_KEY
          valueFrom:
            secretKeyRef:
              name: autoleadgen-secrets
              key: yelp-api-key
        - name: FIRECRAWL_API_KEY
          valueFrom:
            secretKeyRef:
              name: autoleadgen-secrets
              key: firecrawl-api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Service Definition

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: autoleadgen-service
spec:
  selector:
    app: autoleadgen
  type: LoadBalancer
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace autoleadgen

# Create secrets
kubectl create secret generic autoleadgen-secrets \
  --from-literal=yelp-api-key=$YELP_API_KEY \
  --from-literal=firecrawl-api-key=$FIRECRAWL_API_KEY \
  -n autoleadgen

# Apply manifests
kubectl apply -f k8s/ -n autoleadgen

# Check deployment
kubectl get pods -n autoleadgen
kubectl logs -f deployment/autoleadgen -n autoleadgen
```

---

## 📊 Monitoring & Maintenance

### Monitoring with Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'autoleadgen'
    static_configs:
      - targets: ['localhost:8000']
```

### Logging with ELK

```bash
# Docker Compose with ELK
docker-compose -f docker-compose.elk.yml up -d
```

### Health Checks

```python
# src/api/health.py
@app.get("/health")
async def health_check():
    """Check application health."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "services": {
            "database": check_database(),
            "yelp_api": check_yelp_api(),
            "firecrawl": check_firecrawl()
        }
    }
```

### Database Maintenance

```bash
# Backup database
sqlite3 leads.db ".backup leads.db.backup"

# Optimize database
sqlite3 leads.db "VACUUM;"
sqlite3 leads.db "ANALYZE;"

# Cleanup old data
sqlite3 leads.db "DELETE FROM campaigns WHERE created_at < datetime('now', '-90 days');"
```

---

## 🔧 Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check logs
journalctl -u autoleadgen -n 50

# Check port
sudo lsof -i :8000

# Verify configuration
python -c "from autoleadgen.config import Config; print(Config())"
```

#### High Memory Usage
```bash
# Monitor memory
top -p $(pgrep -f autoleadgen)

# Check for leaks
python -m memory_profiler autoleadgen/cli.py

# Reduce concurrency
FIRECRAWL_CONCURRENCY=2
```

#### Database Locked
```bash
# Check connections
lsof /var/lib/autoleadgen/leads.db

# Kill stale connections
pkill -f sqlite3

# Enable WAL mode
sqlite3 leads.db "PRAGMA journal_mode=WAL;"
```

---

## 🚀 Deployment Checklist

- [ ] All environment variables configured
- [ ] API keys set and tested
- [ ] Database initialized and backed up
- [ ] Logs configured and rotating
- [ ] Health checks responding
- [ ] Monitoring set up
- [ ] SSL/TLS certificates valid
- [ ] Rate limiting configured
- [ ] Backup procedures tested
- [ ] Disaster recovery plan documented

---

**Last Updated**: December 2025
