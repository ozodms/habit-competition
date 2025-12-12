# Habit Competition Platform

A Django 6 application for building habit-based challenges, tracking daily progress, and competing on leaderboards.  
Fully containerized with Docker and backed by PostgreSQL.

---

## Key Technologies

- Django 6
- PostgreSQL (psycopg3)
- Gunicorn (production WSGI server)
- Docker + docker-compose
- TailwindCSS (CDN)

---

## Application Architecture

The project is structured as a Django monolith separated into focused apps:

**accounts**  
Registration, login, logout. Signup implemented using Class-Based Views.

**habits**  
CRUD operations for habits. Implemented using ListView, CreateView, UpdateView, and DeleteView.

**challenges**  
Creation, editing, listing and viewing of challenges. Uses CBVs for CRUD and DetailView for public pages.

**participation**  
Functions allowing users to join or leave a challenge. Implemented with function-based views due to side-effect logic.

**tracking**  
Incrementing or decrementing daily habit progress (“check-ins”) inside a challenge. Implemented with FBVs.

**scoring**  
Score aggregation and leaderboard logic, exposed via Class-Based Views.

**core**  
Project-wide settings, root URL routing, and layout templates.

CBVs handle all standard UI flows (forms, lists, detail pages).  
FBVs are used where strict, action-oriented logic is needed (join/leave, plus/minus).

---

## Domain Models (Summary)

**Habit**  
Represents a habit owned by a user or marked as global.  
Includes: owner, is_global, title, description, frequency, max_per_day.

**Challenge**  
A challenge created by a user.  
Includes: created_by, name, slug, description, start_date, end_date, is_public.

**ChallengeHabit**  
Intermediate relation linking habits with challenges.  
Includes: challenge, habit, weight.

**Enrollment**  
Represents a user participating in a challenge.  
Includes: user, challenge, created_at.

**Checkin**  
Tracks daily progress for a habit inside a challenge.  
Includes: enrollment, habit, done_at, quantity.

**ScoreEvent**  
Stores score transactions used for leaderboards.  
Includes: enrollment, points, created_at.

---

## Access Rules

- Users see all global habits and their own personal habits.
- Users can edit or delete only habits they created.
- Only the creator of a challenge can edit it or attach habits to it.
- Public challenges are visible to everyone; private challenges only to the creator.
- Check-in actions (+/−) are available only to users enrolled in the challenge and only within valid challenge dates.

---

## Docker Setup

The project includes:

- `Dockerfile` — Python 3.13 image with Gunicorn entrypoint.
- `docker-compose.yml` — web + PostgreSQL services.
- `entrypoint.sh` — waits for the database, runs migrations, runs collectstatic (prod), starts Gunicorn.
- `.env.example` — environment variable reference.
- `.env.dev` — local development environment (ignored in Git).
