# UWPathr

UWPathr is an open source web application designed to help University of Waterloo CS students plan, explore, and optimize their degree.

The project consists of a **Django + DRF backend** and a **React + Next.js frontend**, with a focus on correctness, robustness, and an intuitive user experience.

More detailed descriptions of the frontend and backend can be found in their respective directories:
`frontend/README.md`
`backend/README.md`

---

## Table of Contents

- [Overview](#overview)
  - [About the Tool](#about-the-tool)
  - [About this README](#about-this-readme)
- [Important Notice](#important-notice)
  - [Prerequisite data](#prerequisite-data)
- [Usage](#usage)
  - [1. Landing page](#1-landing-page)
  - [2. Filling in your checklist](#2-filling-in-your-checklist)
  - [3. Adding courses to your course list](#3-adding-courses-to-your-course-list)
  - [4. Creating a course path](#4-creating-a-course-path)
- [Project Status](#project-status)
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

## Overview

### About the Tool

UWPathr is an open source degree planner for University of Waterloo CS students.

Planning a CS degree is mostly in the hands of the CS student, making it stressful and error-prone. UWPathr simplifies this process by providing a clear degree checklist, automatic prerequisite checking, and tools to plan a valid path to any upper-year course.

What sets UWPathr apart from other degree planners is that it handles course validation automatically. Instead of requiring students to determine whether their course selections are valid, UWPathr enforces degree rules and prerequisites internally, allowing students to focus on exploring courses they’re interested in.

UWPathr is limited to Computer Science degrees, as most other programs at the University of Waterloo are already planned out by the university.

UWPathr currently only supports the base degree (no specialization), but more degrees will come in the future.

### About this README

This file contains instructions about how to use the tool. Below it are setup instructions for anyone who wants to contribute.

For more detailed instructions about the backend and frontend implementation, please visit the their respective READMEs.

---

## Important Notice

### Prerequisite data
To ensure prerequisite data across all courses, generative AI was used to translate web-scraped prerequisite information into a standardized format. This processed data was then used to populate prerequisite entries in the database.

While this approach enables broad coverage and consistency, AI-generated outputs are not guaranteed to be fully accurate. As a result, some course prerequisites may be incorrect.

If you identify a course with incorrect prerequisites, please submit an **“Incorrect Prerequisite”** issue and include the relevant course code.

---

## Usage

### 1. Landing page
- When you enter the site, you are shown the landing page with brief information about UWPathr.
- Create an account and log in. There is currently no email verification.

### 2. Filling in your checklist
- After logging in, you are taken to the dashboard, which displays your degree checklist.
- This checklist matches the official checklists provided by the university.
- For each checkbox, you can add a course by typing its course code and selecting it from the dropdown. Only courses that are valid for that checkbox are shown.
- If you have not completed the required prerequisites for a course, the checklist will prevent you from adding it.
- As you add or remove courses, your progress bar and unit requirements update automatically.
- As with the official university checklists, a course cannot be added to more than one checkbox.
<img width="500" alt="Screenshot 2026-01-11 at 5 24 58 PM" src="https://github.com/user-attachments/assets/33d5e31c-8bc1-4728-8962-f7e01bfc82e0" />
<img width="500" alt="Screenshot 2026-01-11 at 5 29 37 PM" src="https://github.com/user-attachments/assets/b4d036ad-5498-407c-be37-8df518fbf9fc" />

### 3. Adding courses to your course list
- From the dashboard sidebar, navigate to **My Courses**, which contains three lists described on the site.
- You can add a course to a particular list by searching for the course from the sidebar and choosing which list to add it to.
- You can only add courses to your **Taken** list if you have completed the required prerequisites. You may add any course to the **Planned** and **Wishlist** lists.
- When you add a course to a checkbox in your checklist, it is automatically added to your **Taken** list. If you remove it from the checklist, it is not removed from the list and must be removed manually.
<img width="500" alt="Screenshot 2026-01-11 at 5 42 59 PM" src="https://github.com/user-attachments/assets/fc38b417-f570-47dd-b70a-2f13982f3372" />
<img width="500" alt="Screenshot 2026-01-11 at 5 35 53 PM" src="https://github.com/user-attachments/assets/3ac46c96-369f-4d98-b561-4ad5e4bce81e" />

### 4. Creating a course path
- If you want to take an upper-year course but are unsure which prerequisites to choose, add the course to your **Planned** or **Wishlist** list and create a path.
- Clicking this option opens a prerequisite tree that shows the available paths to that course.
- After deciding which path you want to take, select the appropriate branches and click **Save Path**. Your selected branches will change colour to blue.
- You now have a clear list of courses to take in order to reach that upper-year course.
<img width="500" alt="Screenshot 2026-01-11 at 5 36 28 PM" src="https://github.com/user-attachments/assets/3e57a664-fb5d-454e-ab33-ebe767620a0d" />
  
---

## Project Status

- Backend: **actively improving**
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
├── backend/   # Django + DRF backend
├── docs/      # Includes API and database documentation
├── frontend/  # React + Next.js frontend
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
- Backend changes should be discussed before implementation unless the change is simply adding a new API endpoint or serializer.

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


