# Devs Hair and Skin Clinic — Backend (Django + MongoDB Atlas)

## Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # then fill in MONGO_URI and DJANGO_SECRET_KEY
python manage.py migrate   # sets up Django's internal auth/contenttypes tables (SQLite) — required once, not used for app data
```

## Run
```bash
python manage.py runserver
```
API available at http://localhost:8000/api/

## Seed sample data
```bash
python scripts/seed.py
```
Creates staff login: `admin@devsclinic.com` / `Admin@123`, 3 doctors, 5 services, 2 enquiries.

## Email notifications
Every enquiry submitted on `/api/enquiries/` sends an email alert to `CLINIC_NOTIFICATION_EMAIL`
(defaults to `mdhivakar091@gmail.com`). To enable real sending via Gmail:

1. Turn on 2-Step Verification on the sending Gmail account.
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. In `.env`, set:
   ```
   EMAIL_HOST_USER=your-sending-gmail@gmail.com
   EMAIL_HOST_PASSWORD=<16-char app password>
   DEFAULT_FROM_EMAIL=your-sending-gmail@gmail.com
   CLINIC_NOTIFICATION_EMAIL=mdhivakar091@gmail.com
   ```
If these aren't set, emails print to the console instead of failing (safe for local dev).

## Endpoints
See root PROJECT README / API spec doc for full list. Quick reference:
- POST /api/auth/register/  — patient signup
- POST /api/auth/login/     — get JWT pair
- POST /api/auth/refresh/   — refresh access token
- GET/POST /api/doctors/
- GET/PUT/DELETE /api/doctors/{id}/
- GET/POST /api/services/
- GET/PUT/DELETE /api/services/{id}/
- POST /api/enquiries/ (public), GET /api/enquiries/ (staff)
- PATCH /api/enquiries/{id}/ (staff)
- GET/POST /api/bookings/ (authenticated)
- PATCH /api/bookings/{id}/ (staff)

Staff-only endpoints require `Authorization: Bearer <access_token>` from a user with `role: staff`.
