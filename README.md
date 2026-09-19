<div align="center">

# CareerBridge — Campus Placement Portal

**A production-ready, full-stack campus placement management platform**  
for students, companies, and administrators.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=flat-square&logo=flask)
![Vue 3](https://img.shields.io/badge/Vue-3.5-42B883?style=flat-square&logo=vuedotjs&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=flat-square&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-5.6-37814A?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                         CareerBridge                         │
│                                                              │
│  ┌─────────────┐   REST/WS   ┌──────────────────────────┐  │
│  │  Vue 3 SPA  │ ──────────► │  Flask API (Gunicorn)    │  │
│  │  (Vite)     │             │  + Flask-SocketIO        │  │
│  │  Tailwind 4 │             └──────────┬───────────────┘  │
│  └─────────────┘                        │                   │
│                              ┌──────────▼───────────────┐  │
│                              │  PostgreSQL (Neon.tech)   │  │
│                              └──────────────────────────┘  │
│                              ┌──────────────────────────┐  │
│                              │  Redis (Cache + Broker)   │  │
│                              └──────────┬───────────────┘  │
│                              ┌──────────▼───────────────┐  │
│                              │  Celery Worker + Beat     │  │
│                              │  (Background tasks)       │  │
│                              └──────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## Features

### 👨‍🎓 Student
- Register with email OTP or **Google OAuth** (auto-onboarding)
- Multi-step onboarding wizard (academics, skills, resume upload)
- Browse, search, and filter live job listings
- One-click apply with eligibility validation
- Track applications through the full pipeline: `Applied → Shortlisted → Interview → Selected → Placed`
- Interview dates displayed in **IST** (Indian Standard Time)
- Join **native WebRTC video interviews** directly from dashboard
- Upload resume (PDF) and profile picture via Cloudinary
- Weekly email digest of new job openings
- Export application history as CSV (emailed via Celery)

### 🏢 Company
- Register → Admin approval → go live
- Post jobs with salary, CGPA cutoff, branch, and deadline filters
- **Kanban ATS board** — view all applicants organized by pipeline stage
- **Applicant timeline page** — full candidate profile + PDF resume preview
- Move candidates through stages with contextual forms
- Schedule interviews with IST date picker — auto-emails both parties
- Join the **native WebRTC interview room**
- Save private candidate evaluation notes
- Receive monthly placement pipeline reports by email

### 🔑 Admin
- Platform-wide statistics dashboard with charts
- Manage students, companies, jobs, applications, interviews, placements
- Approve/reject company registrations
- Blacklist students or companies
- Full placement tracking

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Flask 3.1, Flask-SocketIO, Flask-JWT-Extended, Flask-Mail, Flask-Caching |
| **Database** | PostgreSQL 14+ + SQLAlchemy ORM |
| **Frontend** | Vue 3, Vue Router, Axios, Vite 8, Tailwind CSS 4 |
| **Real-time** | WebRTC (native browser API) + Socket.IO signaling |
| **Background** | Celery 5.6 + Redis 7 |
| **Scheduler** | Celery Beat (interview reminders, monthly reports, weekly digest) |
| **File Storage** | Cloudinary (resumes, avatars) |
| **Auth** | JWT + Google OAuth 2.0 |
| **Email** | Flask-Mail + Brevo SMTP (300 emails/day free) |
| **Production Server** | Gunicorn + Eventlet |
| **Containerization** | Docker + Docker Compose |
| **Timezone** | All times in **IST (Asia/Kolkata, UTC+5:30)** |

---

## Quick Start — Docker (Recommended)

> **Prerequisites:** Docker Desktop or Docker Engine + Docker Compose

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/careerbridge.git
cd careerbridge

# 2. Set up backend environment
cd backend
cp .env.template .env
# Fill in your values (database URL, email, OAuth, etc.)
cd ..

# 3. One command to run everything
docker compose up --build
```

**That's it.** The full stack is now running:
- **App:** http://localhost
- **API:** http://localhost/api
- **Redis:** localhost:6379

> First run creates the admin account automatically from `ADMIN_EMAIL` and `ADMIN_PASSWORD` in your `.env`.

---

## Quick Start — Manual (4 Terminals)

<details>
<summary>Expand manual setup instructions</summary>

### Prerequisites
| Tool | Version |
|---|---|
| Python | 3.10+ |
| Node.js | 18+ |
| Redis | 7+ |
| PostgreSQL | 14+ (or use Neon.tech free) |

### 1. Backend setup
```bash
cd backend
python -m venv venv
source venv/bin/activate       # Linux/macOS
# venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.template .env          # fill in your values
```

### 2. Frontend setup
```bash
cd frontend
npm install
cp .env.template .env.local    # fill in VITE_API_BASE_URL
```

### 3. Start Redis
```bash
redis-server
# Or: sudo systemctl start redis
```

### 4. Run all services (4 terminals)

```bash
# Terminal 1 — Flask API
cd backend && source venv/bin/activate && python3 run.py

# Terminal 2 — Celery Worker
cd backend && source venv/bin/activate
celery -A celery_worker.celery worker --loglevel=info

# Terminal 3 — Celery Beat (Scheduler)
cd backend && source venv/bin/activate
celery -A celery_worker.celery beat --loglevel=info

# Terminal 4 — Vue Frontend
cd frontend && npm run dev
```

App available at: **http://localhost:5173**

</details>

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `SECRET_KEY` | Flask secret key (random, 32+ chars) | `openssl rand -hex 32` |
| `JWT_SECRET_KEY` | JWT signing key (random, 32+ chars) | `openssl rand -hex 32` |
| `ADMIN_EMAIL` | Auto-created admin account email | `admin@careerbridge.dev` |
| `ADMIN_PASSWORD` | Admin account password | `Admin@Secure123` |
| `REDIS_HOST` | Redis hostname | `localhost` / Upstash host |
| `CELERY_BROKER_URL` | Celery broker (Redis URL) | `redis://localhost:6379/0` |
| `MAIL_SERVER` | SMTP server | `smtp-relay.brevo.com` |
| `MAIL_PORT` | SMTP port | `587` |
| `MAIL_USERNAME` | SMTP username | Brevo login email |
| `MAIL_PASSWORD` | SMTP API key | Brevo SMTP key |
| `MAIL_DEFAULT_SENDER` | From address | `noreply@yourdomain.com` |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | From Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret | From Google Cloud Console |
| `CLOUDINARY_URL` | Cloudinary connection string | `cloudinary://key:secret@cloud` |
| `APP_BASE_URL` | Frontend URL (for email links) | `https://careerbridge.vercel.app` |

### Frontend (`frontend/.env.local`)

| Variable | Description |
|---|---|
| `VITE_API_BASE_URL` | Backend API URL (`http://localhost:5000/api` for local) |
| `VITE_GOOGLE_CLIENT_ID` | Google OAuth client ID (same as backend) |

---

## Deployment (Free Tier)

### Services Used (All Free)
| Service | Purpose | Free Tier |
|---|---|---|
| **Render.com** | Flask API + Celery services | Free (spins down after 15 min idle) |
| **Vercel** | Vue frontend | Free, global CDN |
| **Neon.tech** | PostgreSQL database | Free, serverless |
| **Upstash** | Redis (cache + Celery broker) | 10,000 req/day free |
| **Cloudinary** | File uploads (resumes, avatars) | 25GB storage free |
| **Brevo** | Email (SMTP) | 300 emails/day free |

### Step-by-Step Deployment

#### 1. Database & Redis (External Services)
- **PostgreSQL:** Already on Neon.tech → grab `DATABASE_URL` from dashboard
- **Redis:** Sign up at [Upstash](https://upstash.com) → Create Redis DB → copy `UPSTASH_REDIS_URL`
  - Use this URL as both `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND`

#### 2. Push to GitHub
```bash
# Ensure .env is NOT tracked
git status   # .env should not appear
git add .
git commit -m "chore: production-ready dockerized build"
git push origin main
```

#### 3. Deploy Backend on Render.com
1. Go to [render.com](https://render.com) → **New Web Service**
2. Connect your GitHub repository
3. Set **Root Directory** → `backend`
4. Set **Environment** → `Docker`
5. Set **Start Command** → *(leave blank, the Dockerfile handles it)*
6. Add all environment variables from `backend/.env.template`
7. Deploy → copy the Render URL (e.g., `https://careerbridge-api.onrender.com`)

> **Note:** The Docker container uses `supervisord` to automatically run the Flask API, Celery Worker, and Celery Beat scheduler **inside this single free web service**. You do not need to create separate background workers.

#### 4. Deploy Frontend on Vercel
1. Go to [vercel.com](https://vercel.com) → **New Project** → import GitHub repo
2. Set **Root Directory** → `frontend`
3. Set **Build Command** → `npm run build`
4. Set **Output Directory** → `dist`
5. Add environment variables:
   - `VITE_API_BASE_URL` = `https://careerbridge-api.onrender.com/api`
   - `VITE_GOOGLE_CLIENT_ID` = your Google OAuth client ID
6. Deploy → copy the Vercel URL

#### 5. Final Config Updates
- In Render backend env vars: set `APP_BASE_URL` = your Vercel URL
- In Google Cloud Console: add Vercel URL to authorized JavaScript origins and redirect URIs
- In Flask CORS (already configured for `*` — restrict to Vercel domain for production)

> **Keep Render Awake:** Set up a free cron at [cron-job.org](https://cron-job.org) to ping `https://your-app.onrender.com/` every 14 minutes.

---

## Celery Background Tasks

| Task | Trigger | Description |
|---|---|---|
| `send_otp_email` | On register | Sends email OTP for verification |
| `send_interview_reminders` | Every hour | Emails both student & company for interviews in next 24h |
| `generate_monthly_reports` | 1st of month, 9 AM IST | HTML pipeline report to each company |
| `send_weekly_digest` | Every Monday, 9 AM IST | New job openings email to all students |
| `export_student_applications` | On demand | Emails CSV of applications to student |
| `send_offer_letter_email` | On placement | Emails offer letter PDF to student |

---

## WebRTC Interview System

CareerBridge uses a **100% self-hosted, free** video interview system — no Jitsi, no Agora, no Twilio.

```
Company schedules → Email to both with room link
        ↓
Both open /interview/:applicationId
        ↓
Browser requests camera/mic → Socket.IO signals peers
        ↓
WebRTC RTCPeerConnection → Peer-to-peer video/audio
        ↓
Company evaluates, takes notes → Saved to database
```

**In the interview room:**
- 📹 Full-screen remote video + PiP local preview
- 🎤 Mute/unmute microphone
- 📷 Toggle camera
- 🖥️ Screen share
- ⏱️ Live call timer
- 📝 Private evaluation notes (company only)
- 👤 Candidate resume quick-view

**For internet calls (different networks):** Run the TURN server once:
```bash
sudo bash setup_turn_server.sh
```

---

## Project Structure

```
careerbridge/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── auth_routes.py       # Login, register, Google OAuth, OTP
│   │   │   ├── student_routes.py    # Profile, jobs, applications (cached)
│   │   │   ├── company_routes.py    # Dashboard, ATS, placement
│   │   │   ├── admin_routes.py      # Admin management
│   │   │   └── upload_routes.py     # Cloudinary file uploads
│   │   ├── socket_server.py         # WebRTC signaling (Socket.IO)
│   │   ├── models.py                # SQLAlchemy models (User, Student, Company, Job, Application, Placement)
│   │   ├── tasks.py                 # Celery tasks (email, reports, digest, CSV)
│   │   ├── cache.py                 # Redis cache init
│   │   └── mail.py                  # Flask-Mail init
│   ├── run.py                       # App entrypoint + SocketIO
│   ├── celery_worker.py             # Celery + Beat schedules
│   ├── config.py                    # Config classes (Dev/Prod)
│   ├── gunicorn.conf.py             # Production server config
│   ├── requirements.txt             # Python dependencies
│   ├── Dockerfile                   # Backend Docker image
│   └── .env.template                # Environment variable template
│
├── frontend/
│   ├── src/
│   │   ├── api/axios.js             # Axios instance (VITE_API_BASE_URL)
│   │   ├── router/index.js          # Vue Router + auth guards
│   │   ├── utils/formatDate.js      # IST date formatting helpers
│   │   ├── components/              # Toast, Loader, shared UI
│   │   ├── layouts/                 # StudentLayout, CompanyLayout, AdminLayout
│   │   └── views/
│   │       ├── public_views/        # Login, Register, Landing
│   │       ├── student_views/       # Dashboard, Jobs, Applications, Profile
│   │       ├── company_views/       # Dashboard, ATS, Applicants, Profile
│   │       ├── admin_views/         # All admin pages
│   │       └── InterviewRoom.vue    # WebRTC video call room
│   ├── Dockerfile                   # Multi-stage build (Node → Nginx)
│   └── .env.template                # Frontend env var template
│
├── nginx/
│   └── nginx.conf                   # Reverse proxy (local Docker)
├── docker-compose.yml               # Full stack local dev
├── setup_turn_server.sh             # TURN server for cross-network WebRTC
└── README.md
```

---

## Testing the Full Flow

1. Register a company → Log in as admin → Approve the company
2. Company posts a job (set deadline in future, CGPA, branch)
3. Register a student → Complete onboarding (academics + resume)
4. Student browses jobs → Apply
5. Company → Applicants → Kanban board → Shortlist the student
6. Company → Schedule Interview → pick IST date → both get emails
7. Both open the interview room link → WebRTC call connects
8. Company evaluates → marks Selected → places with joining date → offer letter emailed
9. Admin → Placements → confirms the full cycle

---

## Developed By

**Sayam Ansari**  
Modern Application Development II — IIT Madras BS Degree Program

---

<div align="center">
<sub>All times are in <strong>IST (Indian Standard Time / Asia/Kolkata, UTC+5:30)</strong></sub>
</div>
