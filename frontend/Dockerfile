# ─── CareerBridge Frontend ──────────────────────────────────────────────────
# Multi-stage build:
#   Stage 1 (builder): Node 20 — installs deps, runs vite build → dist/
#   Stage 2 (runtime): Nginx alpine — serves static files from dist/
# Production: Vercel handles this automatically.
# Local dev: docker compose up — this Dockerfile runs locally.
# ────────────────────────────────────────────────────────────────────────────

# ── Stage 1: Build ──────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Install deps first (layer caching)
COPY package.json package-lock.json* ./
RUN npm ci

# Copy source and build
COPY . .

# VITE_API_BASE_URL is passed as a build arg for local Docker
ARG VITE_API_BASE_URL=http://localhost:5000/api
ARG VITE_GOOGLE_CLIENT_ID=""
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_GOOGLE_CLIENT_ID=$VITE_GOOGLE_CLIENT_ID

RUN npm run build

# ── Stage 2: Serve ──────────────────────────────────────────────────────────
FROM nginx:1.27-alpine AS runtime

# Copy nginx config (handles SPA routing + /api proxy)
COPY ../nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built Vue app
COPY --from=builder /app/dist /usr/share/nginx/html

# Health check
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost/ || exit 1

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
