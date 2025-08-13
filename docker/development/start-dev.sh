#!/bin/bash

# Start systemd (required for user slices and resource management)
exec /sbin/init &

# Wait for systemd to initialize
sleep 5

# Start SSH daemon
service ssh start

# Start nginx
nginx -t && service nginx start || (echo "nginx failed to start" && cat /var/log/nginx/error.log || true)

# Start fcgiwrap for CGI (socket at /var/run/fcgiwrap.socket)
service fcgiwrap start || true

# Activate Python virtual environment and start backend services
# Start the backend API server in development mode if present
if [ -f /opt/pubnix/backend/main.py ] || [ -f /opt/pubnix/backend/api/main.py ]; then
  if command -v uvicorn >/dev/null 2>&1; then
    (cd /opt/pubnix/backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload) &
  fi
fi

# Keep container running
tail -f /dev/null