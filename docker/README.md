# ATL Pubnix Docker Configuration

Docker configurations for development and testing environments.

## Components

- `development/` - Local development environment
- `testing/` - Isolated testing environment
- `production/` - Production-like staging environment

## Usage

```bash
# Start development environment
docker-compose -f docker/development/docker-compose.yml up -d

# Run tests in isolated environment
docker-compose -f docker/testing/docker-compose.yml up --abort-on-container-exit

# Production staging
docker-compose -f docker/production/docker-compose.yml up -d
```