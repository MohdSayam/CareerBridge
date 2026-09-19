#!/bin/bash
# Fix TURN server config with correct IP and restart

LOCAL_IP="192.168.1.33"

echo "Configuring TURN server with IP: $LOCAL_IP"

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

# No TLS for local dev
no-tls
no-dtls
EOF

systemctl restart turnserver
sleep 1
systemctl status turnserver --no-pager | head -8

echo ""
echo "TURN server configured for IP: $LOCAL_IP:3478"
echo "Credentials: careerbridge / CareerBridgeTURN2024"
