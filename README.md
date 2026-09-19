# CareerBridge — Campus Placement Portal

Hey there! Welcome to **CareerBridge**, a platform I built for my college project. 

The goal of this project was to build a complete, real-world system that handles the entire campus placement process—from students applying for jobs to companies conducting live video interviews and rolling out offers. 

I wanted to move beyond just writing code and actually experience the full journey: designing the architecture, building the features, and successfully deploying a complex full-stack application to the internet without spending any money!

---

## What does it do?

CareerBridge is divided into three main experiences:

**For Students 👨‍🎓**
- Create a profile, upload a resume, and add your skills.
- Browse live job postings from approved companies.
- Apply for jobs with a single click (if you meet the CGPA/Branch requirements).
- Track your application status (Applied → Shortlisted → Selected).
- Join a live video interview room directly from the browser.
- Get automatic emails when you have an interview or when new jobs are posted.

**For Companies 🏢**
- Post job openings with specific criteria.
- View a clean, drag-and-drop style "Kanban" board to manage applicants.
- Review student profiles and resumes directly on the platform.
- Schedule interviews (which automatically emails the student).
- Conduct live peer-to-peer video interviews.
- Take private evaluation notes during the interview.

**For Admins 🔑**
- See the big picture: how many students are placed, how many jobs are active.
- Approve or reject new company registrations.
- Manage the overall platform safety (blacklisting if necessary).

---

## The Tech Stack

I built this using a modern stack, keeping performance and real-time capabilities in mind:
- **Frontend:** Vue 3, Vite, and Tailwind CSS (Hosted on Vercel)
- **Backend:** Python & Flask (Hosted on Render)
- **Database:** PostgreSQL (Hosted on Neon.tech)
- **Background Tasks:** Celery & Redis (Hosted on Upstash)
- **Real-Time Video:** WebRTC with Socket.IO signaling
- **Emails & Storage:** Brevo (SMTP) and Cloudinary (Resumes/Images)

---

## The Journey: From Local Dev to Global Deployment

Building this locally was one thing, but deploying it to the internet using 100% free-tier services was a massive learning experience! 

1. **The Challenge:** Render's free tier only allows one web service, but my app needed three things running simultaneously: the API, a Celery Worker (for sending emails in the background), and a Celery Beat Scheduler (for recurring tasks like weekly digests).
2. **The Solution:** I Dockerized the backend and used `supervisord` to run all three processes inside a single free container. This completely bypassed the free-tier limitations!
3. **The Database & Cache:** I used serverless PostgreSQL on Neon and Serverless Redis on Upstash. I had to dynamically configure Celery to use TLS (`rediss://`) so it could securely talk to Upstash.
4. **The Frontend:** Deployed the Vue SPA to Vercel, hooking it up to the Render API. I also set up a `vercel.json` rewrite rule to fix SPA routing issues.
5. **The Sleep Problem:** Because Render's free tier goes to sleep after 15 minutes of inactivity, I wrote a Celery task that pings the server every 13 minutes to keep it awake 24/7.

It's now fully live and accessible to anyone!

---

## The WebRTC Interview System

One of the coolest parts of this project is the built-in video interviewing tool. It doesn't use third-party paid APIs like Zoom or Twilio. Instead, it uses **native WebRTC** for true peer-to-peer video calling. 

If you are deploying this yourself for a real production environment, the platform defaults to using Google's free STUN servers (which works for most standard networks). If you want 100% reliability across strict corporate firewalls, you can simply grab a free TURN server from Metered.ca and drop the credentials into the Vercel environment variables (`VITE_TURN_SERVER`).

---

## Want to run it locally?

If you want to spin this up on your own machine, the easiest way is using Docker.

1. Clone this repository.
2. Go to the `backend` folder, copy `.env.template` to `.env`, and fill in your database/email credentials.
3. Run this command:
   ```bash
   docker compose up --build
   ```
4. The app will be running at `http://localhost`.

*Developed by Sayam Ansari for the Modern Application Development II course.*
