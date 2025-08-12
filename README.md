# ATL Pubnix (atl.sh)

A public access Unix system for the All Things Linux community, providing shell accounts, web hosting, and collaborative learning opportunities in a traditional Unix environment.

## Overview

The ATL Pubnix system serves the All Things Linux community by providing:
- Shell accounts with SSH access
- Web hosting capabilities (~username directories)
- Development tools and programming environments
- Community communication features
- Educational resources and documentation

## Architecture

This is a monorepo containing all components of the ATL Pubnix system:

- `backend/` - Core system services and APIs
- `web/` - Web interface and landing pages
- `scripts/` - System administration and deployment scripts
- `config/` - Configuration files and templates
- `docs/` - Documentation and user guides
- `tests/` - Test suites and testing utilities
- `docker/` - Docker configurations for development

## Quick Start

### Development Environment

1. Clone the repository
2. Run the development environment: `docker-compose up -d`
3. Access the web interface at http://localhost:8080
4. SSH to the development pubnix at localhost:2222

### Deployment

See `docs/deployment.md` for production deployment instructions.

## Requirements

- Docker and Docker Compose for development
- Debian-based Linux system for production
- Python 3.9+ for backend services
- Node.js 18+ for web interface build tools

## Contributing

Please read `docs/contributing.md` for development guidelines and contribution process.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Community

- Website: https://atl.sh
- Discord: [All Things Linux Community](https://discord.gg/allthingslinux)
- Documentation: https://docs.atl.sh/pubnix