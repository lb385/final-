# Deployment Guide

## Production Deployment

### Prerequisites

- Docker and Docker Compose
- PostgreSQL 15+ (or use Docker)
- Environment variables configured
- Docker Hub account (for pushing images)

## Deployment Methods

### Method 1: Docker Compose (Recommended for Self-Hosted)

#### Setup

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd final\ project
   ```

2. Create production .env files
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

3. Update environment variables in `.env` files with production values

4. Build images
   ```bash
   docker-compose build
   ```

5. Start services
   ```bash
   docker-compose up -d
   ```

6. Apply migrations
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

7. Check health
   ```bash
   curl http://localhost:8000/health
   ```

#### Monitoring

```bash
# View logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# View container status
docker-compose ps
```

#### Scaling

```bash
# Scale backend instances (requires load balancer)
docker-compose up -d --scale backend=3
```

### Method 2: Docker Hub Deployment

#### Push to Docker Hub

1. Build and tag images
   ```bash
   docker build -f Dockerfile.backend -t yourusername/calculator-backend:1.0.0 .
   docker build -f Dockerfile.frontend -t yourusername/calculator-frontend:1.0.0 .
   ```

2. Login to Docker Hub
   ```bash
   docker login
   ```

3. Push images
   ```bash
   docker push yourusername/calculator-backend:1.0.0
   docker push yourusername/calculator-frontend:1.0.0
   ```

4. Update tags as latest
   ```bash
   docker tag yourusername/calculator-backend:1.0.0 yourusername/calculator-backend:latest
   docker push yourusername/calculator-backend:latest
   ```

#### Deploy from Docker Hub

```bash
# On production server, pull and run
docker run -d \
  -e DATABASE_URL=postgresql://user:pass@db:5432/calculator_db \
  -e SECRET_KEY=your-secret \
  -p 8000:8000 \
  yourusername/calculator-backend:latest

docker run -d \
  -e VITE_API_URL=http://your-domain:8000 \
  -p 3000:3000 \
  yourusername/calculator-frontend:latest
```

### Method 3: Kubernetes Deployment

#### Create Deployment Manifests

Create `k8s/backend-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: calculator-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: calculator-backend
  template:
    metadata:
      labels:
        app: calculator-backend
    spec:
      containers:
      - name: backend
        image: yourusername/calculator-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: secret
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

#### Deploy to Kubernetes

```bash
# Create secrets
kubectl create secret generic db-secret --from-literal=url=postgresql://...
kubectl create secret generic app-secret --from-literal=secret=your-secret-key

# Deploy
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml

# Check status
kubectl get deployments
kubectl get pods
```

## Database Backup and Recovery

### Backup PostgreSQL Database

```bash
# Using pg_dump
pg_dump -U user -d calculator_db > backup.sql

# Or from Docker
docker-compose exec db pg_dump -U user calculator_db > backup.sql
```

### Restore Database

```bash
# Using psql
psql -U user -d calculator_db < backup.sql

# Or from Docker
docker-compose exec -T db psql -U user calculator_db < backup.sql
```

### Scheduled Backups

Create backup script `backup.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec -T db pg_dump -U user calculator_db > "$BACKUP_DIR/backup_$DATE.sql"
```

Schedule with cron:
```bash
0 2 * * * /path/to/backup.sh
```

## Reverse Proxy Setup (Nginx)

Create `nginx.conf`:
```nginx
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:3000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location /api {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## SSL/TLS Setup

### Using Let's Encrypt with Certbot

```bash
# Install Certbot
apt-get install certbot python3-certbot-nginx

# Generate certificate
certbot certonly --standalone -d yourdomain.com

# Update Nginx config with SSL
# In nginx.conf:
server {
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ...
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# Auto-renew certificates
certbot renew --dry-run
```

## Monitoring and Logging

### Application Health Checks

```bash
# Check backend health
curl -X GET http://localhost:8000/health

# Check frontend accessibility
curl -X GET http://localhost:3000
```

### Log Aggregation

Using ELK Stack (Elasticsearch, Logstash, Kibana):

```bash
# Add to docker-compose.yml
services:
  elasticsearch:
    image: elasticsearch:8.0.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"

  logstash:
    image: logstash:8.0.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch

  kibana:
    image: kibana:8.0.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
```

### Monitoring with Prometheus

Add to `docker-compose.yml`:
```yaml
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
```

## Performance Optimization

### Caching

```python
# In backend main.py
from fastapi_cache2 import FastAPICache2
from fastapi_cache2.backends.redis import RedisBackend

# Redis configuration
cache = RedisBackend(redis_client)

@app.get("/api/profile")
@cached(expire=300)  # Cache for 5 minutes
async def get_profile(current_user):
    ...
```

### CDN Integration

Use CloudFront, Cloudflare, or similar CDN for static assets:

```javascript
// In frontend, use CDN URL
const API_URL = process.env.VITE_API_URL || 'https://api.yourdomain.com';
```

## Troubleshooting Deployment Issues

### Service Not Starting

```bash
# Check logs
docker-compose logs backend

# Check service health
docker-compose ps

# Restart service
docker-compose restart backend
```

### Database Connection Issues

```bash
# Check database is running
docker-compose logs db

# Verify credentials in .env
cat backend/.env

# Test connection
docker-compose exec db psql -U user -d calculator_db -c "SELECT 1"
```

### Memory Issues

```bash
# Check resource usage
docker stats

# Limit container memory in docker-compose.yml
services:
  backend:
    mem_limit: 512m
    memswap_limit: 512m
```

### Disk Space

```bash
# Clean up unused containers and images
docker system prune -a

# Check disk usage
docker system df
```

## Secrets Management

### Using Environment Variables

```bash
# Store in .env file (never commit)
export DATABASE_URL=postgresql://user:pass@host:5432/db
export SECRET_KEY=your-secret-key

# Or use Docker secrets (Swarm/Kubernetes)
```

### Using HashiCorp Vault

```bash
# Store secrets in Vault
vault write secret/calculator \
  db_url=postgresql://user:pass@host:5432/db \
  secret_key=your-secret-key

# Retrieve in application
vault read secret/calculator
```

## Disaster Recovery Plan

### Backup Strategy

1. **Daily automated backups** - PostgreSQL dumps to cloud storage
2. **Weekly full backups** - Complete application state
3. **Real-time replication** - Database replication to standby
4. **Version control** - All code in Git with tags

### Recovery Procedure

1. Identify issue and assess data loss
2. Restore from appropriate backup
3. Verify data integrity
4. Update DNS/load balancer if needed
5. Monitor for issues
6. Document incident

See DISASTER_RECOVERY.md for detailed procedures.

## Support

For deployment issues:
- Check logs: `docker-compose logs`
- Review configuration: `cat .env`
- Test connectivity: `curl` and `telnet`
- Contact DevOps team with error messages
