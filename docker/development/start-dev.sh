#!/bin/bash

# Start systemd (required for user slices and resource management)
exec /sbin/init &

# Wait for systemd to initialize
sleep 5

# Start SSH daemon
service ssh start

# Remove any IPv6 listen directives in dev to avoid kernel errors
sed -i '/\[::\]:/d' /etc/nginx/sites-enabled/* 2>/dev/null || true
sed -i '/\[::\]:/d' /etc/nginx/conf.d/*.conf 2>/dev/null || true

# Start nginx
nginx -t && service nginx start || (echo "nginx failed to start" && cat /var/log/nginx/error.log || true)

# Start fcgiwrap for CGI (socket at /var/run/fcgiwrap.socket)
service fcgiwrap start || true

# Activate Python virtual environment and start backend services
# Start the backend API server in development mode if present
if [ -f /opt/pubnix/backend/pyproject.toml ]; then
  if command -v uv >/dev/null 2>&1; then
    (cd /opt/pubnix/backend && uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload) &
  fi
fi

# Keep container running
tail -f /dev/null