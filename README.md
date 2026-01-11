# UWPathr

UWPathr is a web application designed to help University of Waterloo CS students plan, explore, and optimize their degree.

The project consists of a **Django + DRF backend** and a **React + Next.js frontend**, with a focus on correctness, robustness, and an intuitive user experience.

More detailed descriptions of the frontend and backend can be found in their respective directories:
`frontend/README.md`
`backend/README.md`

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Usage](#usage)
- [Project Status](#)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Commands](#commands)
- [Disabled in Development](#disabled-in-development)
- [Contributing](#contributing)
- [Contribution Guidelines](#contribution-guidelines)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Project Status

- Backend: **improving**
- Frontend: **actively improving**
- Contributions: **open and welcome**, especially frontend/UI improvements

---

## Tech Stack

### Backend
- Django
- Django REST Framework
- PostgreSQL

### Frontend
- React
- Next.js

### Auth
- JWT
- Djoser
- OAuth2 (Google)

---

## Project Structure
```text
/
├── backend/    # Django + DRF backend
├── frontend/   # React + Next.js frontend
└── README.md
```

- The **backend** handles all business logic, data validation, and API endpoints.
- The **frontend** consumes the API and focuses on presentation, UX, and accessibility.

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker

### Installation

1. Fork repo.
2. Clone repo and cd to it.
3. Copy .env.example files to .env.development.
   ```Bash
   cp .env.example .env.development
   cp frontend/.env.example frontend/.env.development
   cp backend/.env.example backend/.env.development
   ```
5. Start Docker and build with docker compose in root directory:
   ```Bash
   make build
   ```
7. Verify functionality:
   Go to [http://localhost:3000](http://localhost:3000), create an account, and verify that a checklist is loaded when you log in and that you can search courses.
8. Optional: create a superuser for the django admin:
   `make superuser`
   then login to [http://localhost:8000/admin](http://localhost:8000/admin)

If help is needed, contact suren.v.mar@gmail.com.

### Commands

This project is managed using a `Makefile`. Use the commands below to build and run the project locally.

Docker:
```bash
make up       # Start the containers in detached mode using .env.development
make build    # Build images and start containers using .env.development
make down     # Stop and remove running containers
make down-v   # Stop containers and remove volumes (resets persisted data)
```

Django:
```bash
make superuser   # Creates a django superuser for admin panel
```

---

## Disabled in Development

- OAuth login
- CAPTCHA
- AWS SES (Disabled in production too for now)

---

## Contributing

Contributions are welcome!

- Frontend/UI improvements are especially encouraged
- Backend changes should be discussed before implementation

Please read **[CONTRIBUTING.md](CONTRIBUTING.md)** before opening issues or pull requests.

---

## Contribution Guidelines

- Fork the repository
- Create a feature branch from `main`
- Keep changes focused and scoped
- Open a Pull Request with a clear description
- Include screenshots if necessary for frontend/UI changes

The maintainer reviews and approves all pull requests.

---

## License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

Thanks to everyone who has contributed or shown interest in improving UWPathr.


