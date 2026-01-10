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

1. Create and activate a virtual environment
2. Install dependencies:
   `pip install -r requirements.txt`
3. Configure environment variables
4. Run migrations:
   python manage.py migrate
5. Start the development server:
   python manage.py runserver

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
