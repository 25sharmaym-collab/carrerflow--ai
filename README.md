# CareerFlow AI

Career assistant that compares resumes with job descriptions and produces practical application feedback.

## Current MVP
- Resume text analysis
- PDF/DOCX/TXT parsing API
- Skill normalization and gap detection
- Weighted job-match scoring
- ATS-style checks
- Resume improvement suggestions
- Interview-question generation
- SQLite by default with PostgreSQL-compatible configuration
- Dockerized FastAPI backend
- Next.js frontend

## Architecture

`routes -> schemas -> services -> database`

The analysis engine works without an external AI key. An AI provider can be added through environment configuration without committing secrets.

## Stack

Next.js + TypeScript • FastAPI • SQLAlchemy • PostgreSQL/SQLite • Python • Docker

## Verification

GitHub Actions runs backend pytest and a production frontend build on every push and pull request.

API keys are never committed. Configure local values through `.env` using `.env.example` as the template.
