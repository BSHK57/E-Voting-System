# E-Voting-System

A Django-based E-Voting System for college elections, supporting secure online voting, candidate and voter authentication, and an admin dashboard.

## Features
- User registration and authentication (voters & candidates)
- Admin dashboard for managing elections and approving candidates
- Candidate dashboard with profile editing (party, manifesto, image)
- User dashboard for voting and viewing elections
- Responsive, modern UI with Bootstrap
- Live and completed elections shown on the home page
- Results page for each election (shows top candidate or winner)
- Profile photo support for candidates
- Prevents double voting
- Sample data population script

## How to Run Locally
1. **Clone the repository**
2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```
3. **Apply migrations**
   ```powershell
   python manage.py migrate
   ```
4. **Create a superuser**
   ```powershell
   python manage.py createsuperuser
   ```
5. **Run the development server**
   ```powershell
   python manage.py runserver
   ```
6. **(Optional) Populate sample data**
   ```powershell
   python populate_sample_data.py
   ```
7. **Access the app**
   - Home: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Deployment Notes
- Set `DEBUG = False` and configure `ALLOWED_HOSTS` in `evoting/settings.py`.
- Use Gunicorn + Nginx or a cloud platform for production.
- Run `python manage.py collectstatic` for static files.
- Serve `media/` and `static/` directories via your web server.

## Default Sample Users
- Admin: `admin` / `adminpass`
- User: `user1` / `user1pass`, `user2` / `user2pass`, etc.
- Candidate: `candidate1` / `candidate1pass`, etc.

---

**For college election use. For demo and educational purposes.**
