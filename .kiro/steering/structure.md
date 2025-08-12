# Project Structure & Organization

## Repository Layout

This is a monorepo containing all ATL Pubnix system components:

```
├── backend/              # Python FastAPI backend services
├── web/                  # React TypeScript frontend
├── docker/               # Docker configurations
│   ├── development/      # Local development environment
│   └── testing/          # Isolated testing environment
├── config/               # System configuration files
│   ├── nginx/            # Nginx web server configs
│   └── ssh/              # SSH daemon configurations
├── scripts/              # System administration scripts
│   └── database/         # Database initialization and migrations
├── docs/                 # Documentation and user guides
├── tests/                # Cross-component integration tests
└── .kiro/                # Kiro AI assistant configuration
    └── steering/         # AI guidance rules
```

## Backend Structure

```
backend/
├── user_management/      # User account provisioning and management
├── resource_monitor/     # Resource usage monitoring and enforcement
├── web_hosting/          # Web hosting service configuration
├── security/             # Security monitoring and intrusion detection
├── communication/        # Inter-user communication features
├── admin/                # Administrative tools and interfaces
├── api/                  # REST API for web interface integration
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
└── requirements-test.txt # Testing dependencies
```

## Configuration Management

- **Development configs**: Located in `config/` with `_dev` suffix
- **Production configs**: Templates without suffix, deployed separately
- **Environment-specific**: Use environment variables for sensitive data
- **Docker configs**: Separate compose files for dev/test/prod environments

## File Naming Conventions

- **Python**: snake_case for modules, PascalCase for classes
- **JavaScript/TypeScript**: camelCase for variables/functions, PascalCase for components
- **Config files**: kebab-case with environment suffix (e.g., `nginx_dev.conf`)
- **Docker files**: `Dockerfile.service` format
- **Scripts**: Executable with `.sh` extension

## Development Workflow

1. **Local Development**: Use `docker/development/` for full stack
2. **Testing**: Use `docker/testing/` for isolated test runs
3. **Database Changes**: Create Alembic migrations in `backend/`
4. **Frontend Changes**: Hot reload via Vite dev server on port 3000
5. **System Config**: Modify files in `config/` and rebuild containers

## Key Directories

- **`/home`**: User home directories (mounted volume in containers)
- **`/var/log/pubnix`**: Application logs (mounted volume)
- **`/opt/pubnix`**: Application installation directory in containers
- **`~username`**: User web directories served by nginx

## Resource Organization

- **Static Assets**: Served directly by nginx
- **User Content**: Isolated in individual home directories
- **Application Data**: PostgreSQL database with proper indexing
- **Cache Data**: Redis for sessions and temporary data
- **Logs**: Structured logging with different levels per environment

## Security Boundaries

- **User Isolation**: Each user has separate home directory and resource limits
- **Process Isolation**: Docker containers for service separation
- **Network Isolation**: Docker networks for internal communication
- **File Permissions**: Proper Unix permissions and ownership
- **Database Access**: Connection pooling with limited privileges

## Testing Structure

- **Unit Tests**: Component-specific in respective directories
- **Integration Tests**: Cross-component in `tests/` directory
- **System Tests**: Full stack testing via Docker compose
- **SSH Tests**: Automated connection and functionality testing