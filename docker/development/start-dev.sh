#!/bin/bash

# Start systemd (required for user slices and resource management)
exec /sbin/init &

# Wait for systemd to initialize
sleep 5

# Start SSH daemon
service ssh start

# Start nginx
service nginx start

# Start rsyslog
service rsyslog start

# Activate Python virtual environment and start backend services
cd /opt/pubnix/backend
source venv/bin/activate

# Start the backend API server in development mode
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &

# Start resource monitoring daemon
python -m resource_monitor.daemon --dev &

# Keep container running
tail -f /dev/null