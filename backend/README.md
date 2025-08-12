# ATL Pubnix Backend

Core system services and APIs for the ATL Pubnix system.

## Components

- `user_management/` - User account provisioning and management
- `resource_monitor/` - Resource usage monitoring and enforcement
- `web_hosting/` - Web hosting service configuration
- `security/` - Security monitoring and intrusion detection
- `communication/` - Inter-user communication features
- `admin/` - Administrative tools and interfaces
- `api/` - REST API for web interface integration

## Development

```bash
cd backend
uv sync --dev
uv run pytest tests/
uv run ruff check .
uv run ruff format .
```