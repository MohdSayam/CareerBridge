# Gunicorn production config for CareerBridge
# Flask-SocketIO requires eventlet worker class

import os

# Workers: keep low on free Render tier (0.1 vCPU shared)
workers = int(os.environ.get("GUNICORN_WORKERS", 2))

# eventlet is required for Flask-SocketIO (WebRTC signaling)
worker_class = "eventlet"

# Bind to 0.0.0.0 so Docker/Render can expose it
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"

# Timeouts — increase for slow cold starts on Render free tier
timeout = 120
keepalive = 5

# Logging
accesslog = "-"   # stdout
errorlog = "-"    # stderr
loglevel = os.environ.get("LOG_LEVEL", "info")
