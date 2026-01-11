# Backend (Django + DRF)

This directory contains the backend for UWPathr.

The backend is responsible for:
- Business logic
- Data validation
- Authentication and permissions
- API endpoints consumed by the frontend

---

## Tech Stack
- Python
- Django
- Django REST Framework
- Djoser
- PostgreSQL

---

## Project Structure (High Level)
```text
backend/
├── checklist/       # App: Default checklist templates
├── core/            # Project settings
├── courses/         # App: Course data
├── progress/        # App: User progress (selected courses, checklist, etc)
├── users/           # App: User accounts
├── manage.py
└── requirements.txt
```
(Exact structure may vary.)

---

## Setup (Local Development)

1. Fork and clone repo
2. Rename .env.example to .env
3. Start Docker Engine and build with docker compose in root directory:
   `docker compose up --build -d`
4. Verify functionality:
   Go to [http://localhost:3000](http://localhost:3000), create an account, and verify that a checklist is loaded and that you can search courses.
5. Optional: create a superuser for the django admin:
   `docker compose exec backend python manage.py createsuperuser`
   then login to [http://localhost:8000/admin](http://localhost:8000/admin)

---

## Environment Variables

### Required
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` — PostgreSQL config
- `DJANGO_SECRET_KEY` — Django secret key

### Optional (Safe Defaults Provided)
- `DEBUG` — Django debug mode (default: True for dev)
- `CAPTCHA_ENABLED` — Enable Turnstile CAPTCHA on signup (default: False). Set to True in production.
- `OAUTH2_ENABLED` — Enable Google OAuth2 (default: False). Set to True in production
- `AWS_SES_ENABLED` — Enable AWS SES for email (default: False)

**Note:** Contributors don't need to set optional env vars. Development works without them.

If help is needed, contact suren.v.mar@gmail.com.

---

## API Usage

- The backend exposes a REST API consumed by the frontend
- API endpoints and expected payloads are defined in the Django apps
- Authentication and permissions are enforced at the API level

---

## Contributing to the Backend

Backend contributions are limited and should be discussed before implementation.

Please:
- Open an issue before making significant backend changes
- Avoid changing API behavior without discussion
- Avoid refactoring core backend logic unless explicitly approved

For full contribution rules, see the root CONTRIBUTING.md file.

---

## Notes for Contributors

- The backend prioritizes correctness and stability over rapid iteration
- Not all backend pull requests may be accepted
- Small fixes may be accepted; architectural changes require discussion

---

## License

This backend is licensed under the MIT License.  
See the root LICENSE file for details.
