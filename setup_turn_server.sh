#!/bin/bash
# CareerBridge TURN Server - One-time Setup
# Run this with sudo to install and start the TURN server

echo "=== CareerBridge TURN Server Setup ==="

# Install coturn
pacman -S coturn --noconfirm

# Get the local IP (compatible with Arch/Manjaro)
LOCAL_IP=$(ip route get 1 | awk '{print $7; exit}' 2>/dev/null || ip addr show | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | cut -d/ -f1 | head -1)
echo "Detected local IP: $LOCAL_IP"

# Create the configuration
cat > /etc/turnserver.conf << EOF
listening-port=3478
tls-listening-port=5349
listening-ip=$LOCAL_IP
relay-ip=$LOCAL_IP

# Credentials for WebRTC
user=careerbridge:CareerBridgeTURN2024
realm=careerbridge.local

# Security
lt-cred-mech
fingerprint

# Logging
log-file=/var/log/turnserver.log
verbose

# No TLS for local dev (add certs for production)
no-tls
no-dtls
EOF

echo "Configuration written to /etc/turnserver.conf"

# Enable and start the service
systemctl enable coturn
systemctl start coturn

echo ""
echo "TURN server is running on $LOCAL_IP:3478"
echo "Credentials: careerbridge / CareerBridgeTURN2024"
echo ""
echo "Add this to your frontend .env or config:"
echo "VITE_TURN_SERVER=turn:$LOCAL_IP:3478"
echo "VITE_TURN_USERNAME=careerbridge"
echo "VITE_TURN_CREDENTIAL=CareerBridgeTURN2024"
