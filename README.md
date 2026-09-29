<div align="center">

# CareerBridge — Campus Placement Portal

**A full-stack campus placement management platform built by a student, for students.**

🌐 **[Live Demo → frontend-zeta-opal-iuysvy4bmk.vercel.app](https://frontend-zeta-opal-iuysvy4bmk.vercel.app)**
&nbsp;·&nbsp;
🎬 **[Watch Product Demo →](#)** *(video coming soon)*

> ⚡ **First-time visitors:** The backend is hosted on Render's free tier and goes to sleep after 15 minutes of inactivity. Your **very first action** (login, register, etc.) might take up to **60 seconds** to respond while the server wakes up. Just wait — don't refresh — and after that everything is fast and normal!

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=flat-square&logo=flask)
![Vue 3](https://img.shields.io/badge/Vue-3.5-42B883?style=flat-square&logo=vuedotjs&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Upstash-DC382D?style=flat-square&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-5.6-37814A?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![Deployed on Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=flat-square&logo=render&logoColor=white)
![Deployed on Vercel](https://img.shields.io/badge/Deployed_on-Vercel-000000?style=flat-square&logo=vercel)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## What is CareerBridge?

CareerBridge is a complete campus placement management platform I built for my Modern Application Development college project. The goal was simple: our college placement process was fragmented — students tracked applications on spreadsheets, companies emailed résumés back and forth, and admins had no central visibility. I wanted to fix that by building a real, production-ready system.

The result is a full-stack web application where **students** can apply for jobs and join live video interviews, **companies** can post jobs and manage their entire hiring pipeline, and **administrators** can oversee everything from a central dashboard — all in one place, accessible from any browser.

> **Tried it yet?** Visit the live deployment: [frontend-zeta-opal-iuysvy4bmk.vercel.app](https://frontend-zeta-opal-iuysvy4bmk.vercel.app)

---

## Features by Role

### 👨‍🎓 For Students
- Register with email OTP verification or Google OAuth
- Build a detailed profile (education, branch, CGPA, skills, resume upload)
- Browse a job board that **only shows jobs you are eligible for** (based on your CGPA, branch, and graduation year)
- Apply for jobs with a single click
- Track every application through its pipeline stages — Applied → Shortlisted → Interview → Selected
- See your upcoming interview date with a countdown right on the dashboard
- **Join live video interviews directly in the browser** — no Zoom, no Google Meet needed
- Receive automatic email notifications for interview schedules and new job postings

### 🏢 For Companies
- Register and wait for admin approval (so the platform stays quality-controlled)
- Post detailed job listings with specific eligibility criteria (CGPA cutoff, branch, experience level)
- View all applicants for each job with their profiles and résumés — inline, without downloading
- Drag-and-drop style Kanban pipeline to move candidates between stages
- Schedule interview date and time, which automatically sends a calendar email to the student
- Conduct a live peer-to-peer video interview in the browser
- Take private notes during the interview that only the company can see
- Mark candidates as Selected/Rejected right inside the interview room

### 🔑 For Administrators
- Dedicated admin dashboard with global statistics
- See total students placed, active jobs, pending applications, and revenue metrics at a glance
- Approve or reject new company registrations
- Blacklist students or companies if needed
- Automatic weekly placement digest emails sent every Monday
- Automated monthly CSV reports of placement activity

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Frontend** | Vue 3 + Vite + Tailwind CSS | Fast SPA with component-driven UI |
| **Backend** | Python + Flask + Flask-SocketIO | Lightweight API with real-time support |
| **Database** | PostgreSQL (Neon) | Relational data with serverless free tier |
| **Cache & Queue** | Redis (Upstash) | Celery broker for background jobs |
| **Background Tasks** | Celery + Celery Beat | Async emails, scheduled reports |
| **Video Calling** | Native WebRTC + Socket.IO signaling | P2P video with no third-party API costs |
| **File Storage** | Cloudinary | Resume and profile picture uploads |
| **Email** | Brevo SMTP | 300 free emails/day, very reliable |
| **Auth** | JWT + Google OAuth | Secure, stateless sessions + social login |
| **Process Manager** | Supervisord | Runs Flask + Celery + Beat in one container |
| **Frontend Host** | Vercel | Free, instant global CDN |
| **Backend Host** | Render | Free Docker container hosting |

---

## Architecture Overview

```
Browser (Vue 3 SPA on Vercel)
    │
    ├── REST API → Flask (Gunicorn + Eventlet)  ─── PostgreSQL (Neon)
    │                   │
    │                   ├── Socket.IO (WebRTC signaling for video)
    │                   └── Celery Tasks → Redis (Upstash)
    │                           │
    │                           ├── send_otp_email_task
    │                           ├── interview_reminder_task
    │                           ├── weekly_job_digest_task
    │                           ├── monthly_placement_report_task
    │                           └── offer_letter_task
    │
    └── Cloudinary (resume / profile picture uploads)
```

**The clever deployment trick:** Render's free tier only allows one web service, but this app needs three processes (Flask API, Celery Worker, Celery Beat Scheduler). The solution: Dockerize the backend and use **Supervisord** to run all three processes inside a single container. This made a complex architecture fit perfectly on the free tier.

---

## The Real-Time Video Interview System

One of the coolest parts of CareerBridge is the built-in video interviewing tool.

It does **not** use paid APIs like Zoom, Twilio, or Agora. Instead, it uses native **WebRTC** for true peer-to-peer video calls, with a Socket.IO server handling the "signaling" (the initial connection handshake between two browsers). Once connected, video and audio stream directly between the two devices — the server is not involved.

```
Student Browser ←── WebRTC P2P stream ──→ Company Browser
                         ↑
               Socket.IO signaling (Flask)
               Handles: join_room, offer, answer, ICE candidates
```

**Interview room features:**
- Toggle camera and microphone on/off
- Screen sharing (company can ask student to share their code editor)
- Call duration timer
- Company: take private notes during the call
- Company: update candidate status (Shortlisted/Selected/Rejected) directly from the room

---

## Project Structure

```
CareerBridge/
├── backend/
│   ├── app/
│   │   ├── models.py              # SQLAlchemy DB models
│   │   ├── routes/
│   │   │   ├── auth_routes.py     # Register, Login, Google OAuth, OTP
│   │   │   ├── student_routes.py  # Student dashboard, applications, profile
│   │   │   ├── company_routes.py  # Company dashboard, jobs, applicants
│   │   │   └── admin_routes.py    # Admin dashboard, approvals
│   │   ├── tasks.py               # All Celery background tasks
│   │   ├── socketio_events.py     # WebRTC signaling events
│   │   ├── mail.py                # Flask-Mail init
│   │   └── cache.py               # Flask-Caching (Redis) init
│   ├── celery_worker.py           # Celery app + beat schedule config
│   ├── run.py                     # Flask app factory + SocketIO init
│   ├── config.py                  # Environment-based configuration
│   ├── gunicorn.conf.py           # Gunicorn + eventlet config for SocketIO
│   ├── supervisord.conf           # Runs gunicorn + celery-worker + celery-beat
│   ├── Dockerfile                 # Single container for all 3 backend processes
│   ├── requirements.txt
│   └── .env.sample                # ← Copy this to .env and fill in your values
│
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── public_views/      # Home, Login, Register
│   │   │   ├── student_views/     # Dashboard, Jobs, Applications, Profile
│   │   │   ├── company_views/     # Dashboard, Job Board, Applicants, Interviews
│   │   │   ├── admin_views/       # Admin dashboard and approvals
│   │   │   └── InterviewRoom.vue  # WebRTC video call room (used by both roles)
│   │   ├── router/index.js        # Vue Router with role-based guards
│   │   ├── api/axios.js           # Axios instance with JWT interceptor
│   │   └── utils/formatDate.js    # IST date formatting helper
│   ├── .env.template              # ← Copy this to .env.local and fill in values
│   └── vercel.json                # SPA rewrite rule so page refresh works on Vercel
│
├── docker-compose.yml             # Local dev: one command to run everything
└── README.md
```

---

## Running Locally

The easiest way is Docker. It starts everything (Redis, Flask, Celery, Vue) with one command.

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### Steps

**1. Clone the repo**
```bash
git clone https://github.com/MohdSayam/CareerBridge.git
cd CareerBridge
```

**2. Set up the backend environment**
```bash
cd backend
cp .env.sample .env
# Now open .env in any editor and fill in your credentials
# (Database URL, SMTP keys, Google OAuth ID, Cloudinary URL, etc.)
```

**3. Set up the frontend environment**
```bash
cd ../frontend
cp .env.template .env.local
# Open .env.local and set:
# VITE_API_BASE_URL=http://localhost:5000/api
# VITE_GOOGLE_CLIENT_ID=your-google-client-id
```

**4. Start everything**
```bash
cd ..
docker compose up --build
```

**5. Open your browser**
- Frontend: [http://localhost](http://localhost)
- Backend API: [http://localhost:5000/api](http://localhost:5000/api)

> The first time you run it, Docker will download images and install dependencies. This takes 2–3 minutes. After that, subsequent starts are very fast.

### Running without Docker (manual)

If you prefer not to use Docker:

```bash
# Terminal 1 — Start Redis (or use Upstash)
redis-server

# Terminal 2 — Start Flask
cd backend
pip install -r requirements.txt
python run.py

# Terminal 3 — Start Celery Worker
cd backend
celery -A celery_worker.celery worker --loglevel=info

# Terminal 4 — Start Celery Beat
cd backend
celery -A celery_worker.celery beat --loglevel=info

# Terminal 5 — Start Vue frontend
cd frontend
npm install
npm run dev
```

---

## Deploying Your Own Instance

This project is deployed 100% on free tiers. Here is the exact stack I used:

| Service | Provider | Cost | What it does |
|---------|----------|------|-------------|
| PostgreSQL | [Neon](https://neon.tech) | Free | Database |
| Redis | [Upstash](https://upstash.com) | Free | Celery broker + cache |
| Backend | [Render](https://render.com) | Free | Flask + Celery (Docker) |
| Frontend | [Vercel](https://vercel.com) | Free | Vue SPA |
| Email | [Brevo](https://brevo.com) | Free (300/day) | OTP + notification emails |
| Images | [Cloudinary](https://cloudinary.com) | Free | Résumés + profile pictures |
| Google Auth | [Google Cloud Console](https://console.cloud.google.com) | Free | OAuth 2.0 |

> **Important for Render:** When you create a new Web Service, point it to this repo, select **Docker** as the runtime, and add all your `.env` variables in the Render dashboard "Environment" tab. Render will automatically detect the `Dockerfile` and deploy it.

> **Important for Vercel:** Add `VITE_API_BASE_URL` and `VITE_GOOGLE_CLIENT_ID` in your Vercel project's Environment Variables settings before deploying.

---

## Free Tier Considerations

Since everything runs on free plans, here are a few things to know:

- **Render sleeps after 15 min of inactivity.** The first request after a sleep takes ~30–60 seconds to respond. This is normal. Subsequent requests are fast.
- **Upstash Redis has a 10,000 command/day limit.** Because Celery only runs when Render is awake, and the app goes to sleep when idle, you will almost never hit this limit for a college project.
- **Brevo gives 300 emails/day.** More than enough unless you somehow get 300 people registering in a single day.
- **Neon gives 0.5 GB of storage.** Text data is tiny. 0.5 GB is enough for hundreds of thousands of users.

---

## Environment Variables Reference

### Backend (`backend/.env`)

| Variable | Description | Where to get it |
|----------|-------------|-----------------|
| `DATABASE_URL` | PostgreSQL connection string | [neon.tech](https://neon.tech) |
| `SECRET_KEY` | Flask session secret (any random string) | Generate randomly |
| `JWT_SECRET_KEY` | JWT signing key (any random string) | Generate randomly |
| `CELERY_BROKER_URL` | Redis URL with `rediss://` prefix | [upstash.com](https://upstash.com) |
| `CELERY_RESULT_BACKEND` | Same as broker URL | [upstash.com](https://upstash.com) |
| `MAIL_SERVER` | SMTP server host | [brevo.com](https://brevo.com) |
| `MAIL_USERNAME` | SMTP login email | [brevo.com](https://brevo.com) |
| `MAIL_PASSWORD` | SMTP key | [brevo.com](https://brevo.com) |
| `MAIL_DEFAULT_SENDER` | Sender email address | Your email |
| `GOOGLE_CLIENT_ID` | OAuth 2.0 Client ID | [console.cloud.google.com](https://console.cloud.google.com) |
| `CLOUDINARY_URL` | Full Cloudinary URL | [cloudinary.com](https://cloudinary.com) |
| `ADMIN_EMAIL` | Initial admin account email | Your choice |
| `ADMIN_PASSWORD` | Initial admin account password | Your choice |
| `APP_BASE_URL` | Your frontend URL (for email links) | Your Vercel URL |

### Frontend (`frontend/.env.local`)

| Variable | Description |
|----------|-------------|
| `VITE_API_BASE_URL` | Backend API URL (e.g. `https://your-app.onrender.com/api`) |
| `VITE_GOOGLE_CLIENT_ID` | Same Google OAuth Client ID as backend |
| `VITE_TURN_SERVER` | (Optional) TURN server URL for strict firewall environments |
| `VITE_TURN_USERNAME` | (Optional) TURN server username |
| `VITE_TURN_CREDENTIAL` | (Optional) TURN server credential |

---

## Registration Flow (OTP Verification)

The registration process is designed so **no unverified user ever touches the database**:

1. User fills in name, email, password on the registration form.
2. Backend generates an OTP and stores the pending registration in **Redis** with a 10-minute expiry. Nothing goes into PostgreSQL yet.
3. OTP email is sent asynchronously via Celery (so the API responds instantly, no timeout).
4. User enters the OTP on the next screen.
5. Only after a correct OTP is submitted does the backend create the user record in PostgreSQL.

This means abandoned registrations automatically disappear from Redis after 10 minutes — no cleanup job needed.

---

## API Endpoints (Summary)

<details>
<summary><strong>Auth Routes</strong> — <code>/api/auth</code></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Start registration (sends OTP to Redis) |
| POST | `/verify-email` | Submit OTP, create user in DB |
| POST | `/login` | Email + password login |
| POST | `/google/login` | Google OAuth login |

</details>

<details>
<summary><strong>Student Routes</strong> — <code>/api/student</code></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard` | Student dashboard stats |
| GET | `/jobs` | Jobs the student is eligible for |
| POST | `/apply/:job_id` | Apply for a job |
| GET | `/applications` | All student applications with status |
| GET/PUT | `/profile` | Get or update student profile |

</details>

<details>
<summary><strong>Company Routes</strong> — <code>/api/company</code></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard` | Company dashboard stats |
| POST | `/jobs` | Post a new job |
| GET | `/applicants` | All applicants across all jobs |
| PATCH | `/application/:id` | Update applicant status / schedule interview |
| GET/PUT | `/profile` | Get or update company profile |

</details>

<details>
<summary><strong>Admin Routes</strong> — <code>/api/admin</code></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard` | Platform-wide statistics |
| GET | `/companies/pending` | Companies awaiting approval |
| POST | `/company/:id/approve` | Approve a company |
| POST | `/company/:id/reject` | Reject a company |

</details>

---

## License

This project is open source under the [MIT License](LICENSE). Feel free to fork it, adapt it, and build your own placement portal on top of it. A credit in your README is always appreciated!

---

<div align="center">

Built with a lot of ☕ and debugging sessions by **Sayam Ansari**

*Modern Application Development II — College Project*

</div>
