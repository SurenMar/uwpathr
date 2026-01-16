# Contributing Guide

Thanks for your interest in contributing to **UWPathr**!
Contributions are welcome, especially improvements to the frontend and UI.

This document explains **how to contribute**, **what kinds of contributions are encouraged**, and **the rules we follow** to keep the project maintainable.

---

## Table of Contents
- [Ways to Contribute](#ways-to-contribute)
- [Project Structure](#project-structure)
- [Before You Start](#before-you-start)
- [Issues](#issues)
- [Pull Requests](#pull-requests)
- [Frontend Contributions](#frontend-contributions)
- [Backend Contributions](#backend-contributions)
- [Code Style & Expectations](#code-style--expectations)

---

## Ways to Contribute

You can contribute by:
- Reporting/Fixing bugs
- Improving the UI / UX
- Adding new features
- Adding new backend api endpoints or serializers
- Displaying new content
- Improving performance or accessibility
- Improving documentation

---

## Project Structure
```text
/
├── backend/    # Django + DRF backend
├── frontend/   # React + Next.js frontend
└── README.md
```

- The backend is improving and welcomes contributions.
- The frontend is the primary area open for community contributions.

---

## Before You Start

- Please comment on an issue before starting work so others know it’s being worked on.
- For larger changes, open an issue first to discuss the approach.
- Small fixes (UI tweaks, typos, minor bugs) can go straight to a PR.

---

## Issues

### Reporting a Bug
When opening a bug report, please include:
- What happened
- What you expected to happen
- Steps to reproduce
- Screenshots or screen recordings if applicable (especially for frontend issues)

### Feature Requests
Feature requests are welcome, especially frontend improvements.

Please explain:
- The problem you’re trying to solve
- Why it’s useful
- Any UI ideas or references (screenshots, mockups, etc.)

### Incorrect Prerequisites
If you find a course has incorrect prerequisites, just include the course code in the issue.
The correct prerequisites will be added to the database, meaning developers may need to re-run initialize_db.sh if the needed.

---

## Pull Requests

### Basic Flow
1. Fork the repository
2. Clone your fork
3. Create a new branch from `main`

   `git checkout -b feature/short-description`

4. Make your changes
5. Commit with a clear message
6. Push your branch
7. Open a Pull Request against `main`

Please read the [Pull Request requirements](./.github/pull_request_template.md) before opening a PR.

---

## Frontend Contributions

Frontend contributions are especially welcome.

Guidelines:
- Focus on UI, UX, accessibility, and responsiveness
- Avoid changing backend APIs unless discussed first
- Keep changes scoped and focused
- You do not need backend knowledge to contribute to the frontend

---

## Backend Contributions

Backend changes should be discussed before starting work unless it's simply adding a new API endpoint or serializer.

Please open an issue first if you want to:
- Heavy modifications to an existing API endpoint behavior
- Change authentication or permissions
- Change database models
- Refactor backend architecture

Otherwise, if you need to add a new API endpoint or serializer while working on a frontend feature, posting an issue is not required.

---

## Code Style & Expectations

- Keep changes focused and readable
- Avoid large, unrelated refactors
- Write descriptive commit messages
- Be respectful in discussions

---

## Thank You!

Thanks for taking the time to contribute!
Your help is appreciated and helps improve the project for everyone.

### Contributors:
<a href="https://github.com/SurenMar">
  <img
    src="https://avatars.githubusercontent.com/SurenMar"
    alt="SurenMar's Profile Picture"
    width="100"
    height="100"
  />
</a>


