# ResumeSense — Professional ATS Resume & Presentation Analyzer

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Backend](https://img.shields.io/badge/backend-Django%205%20%2B%20DRF-blue.svg)]()
[![Frontend](https://img.shields.io/badge/frontend-React%20%2B%20TypeScript%20%2B%20Tailwind-61dafb.svg)]()
[![Database](https://img.shields.io/badge/database-PostgreSQL%20%2F%20SQLite-336791.svg)]()

**ResumeSense** is an enterprise-grade AI-assisted document analysis SaaS platform. It evaluates resumes and presentation files for ATS-style readability, section structure integrity, typography compatibility, keyword alignment, and job description match without relying on simulated random scores.

Designed with a **Microsoft / Adobe-inspired SaaS aesthetic**, ResumeSense presents clean data density, circular score gauges, slide-by-slide diagnostics, and downloadable branded PDF reports.

---

## 🚀 Key Features

- **Multi-Format Document Parsing**: Native structural parsing for **PDF** (PyMuPDF), **DOCX** (python-docx), and **PPT / PPTX** (python-pptx).
- **Transparent ATS Compatibility Scoring**: Deterministic, weighted evaluation across:
  - **Text Extraction Quality** (25%)
  - **Section Structure Integrity** (20%)
  - **Typography & Formatting** (20%)
  - **Keyword & Competency Coverage** (20%)
  - **Contact Information Completeness** (15%)
- **Slide-by-Slide PPT Diagnostics**: Detects text trapped inside screenshots/images, tiny fonts (<10pt), complex shapes, and text density anomalies.
- **Job Description Matcher**: Compares candidate resumes against target job descriptions using keyword overlap and semantic vector similarity.
- **Categorized Actionable Findings**: Highlights issues categorized by severity:
  - 🔴 **Critical**: Missing essential keywords or images inside critical sections.
  - 🟠 **Important**: Non-standard headings, missing contact details, or dense bullet points.
  - 🔵 **Suggestion**: Typography recommendations and layout optimizations.
  - 🟢 **Good**: Positive structural checks passed.
- **Extracted Text Transparency**: Inspect the exact plain text extracted by automated applicant tracking parsers.
- **Downloadable PDF Reports**: Export branded executive summary reports generated with ReportLab.
- **User Dashboard & File Management**: Full file lifecycle management, lifetime statistics, and analysis history.
- **Pre-seeded Sample Demo**: Instant "Try Sample" workflow with the complete sample profile and score data.

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 19 + TypeScript + Vite
- **Styling**: Tailwind CSS v4 with professional SaaS tokens
- **Icons**: Lucide React
- **Visuals**: Animated SVG Circular Gauges, Progress Bars
- **Routing**: React Router v7
- **HTTP Client**: Axios with JWT Bearer injection & refresh interceptors

### Backend
- **Framework**: Python 3.12+ / 3.14, Django 5.x, Django REST Framework
- **Authentication**: JWT (`djangorestframework-simplejwt`) with refresh rotation
- **Document Parsing**:
  - `PyMuPDF` (`fitz`) for PDF text blocks, fonts, and images
  - `python-docx` for Word headings, tables, styles, and body text
  - `python-pptx` for PowerPoint slides, text boxes, and shapes
  - `Pillow` & `pytesseract` for image OCR fallback
- **NLP & Analysis**:
  - `scikit-learn` & `scipy` for TF-IDF vectorization and cosine similarity
  - `sentence-transformers` for semantic embeddings
  - Comprehensive technical, soft skills, and tool taxonomies
- **Reporting**: ReportLab PDF generator

### Infrastructure & Database
- **Database**: PostgreSQL 16 (production/Docker) & SQLite3 (instant local dev)
- **Containerization**: Docker & Docker Compose
- **Web Server**: Gunicorn & Nginx

---

## 📐 ATS Scoring Methodology

ResumeSense calculates a transparent, weighted **ATS Compatibility Score (0–100)**:

$$\text{Score} = (0.25 \times \text{Text}) + (0.20 \times \text{Structure}) + (0.20 \times \text{Format}) + (0.20 \times \text{Keywords}) + (0.15 \times \text{Contact})$$

| Category | Weight | Evaluation Criteria |
|---|---|---|
| **Text Extraction** | 25% | OCR requirements, encoding issues, garbage characters, extractable word counts |
| **Section Structure** | 20% | Standard headings (Experience, Education, Skills, Projects), chronological layout |
| **Formatting** | 20% | Standard fonts (Arial, Calibri, Times), multi-page density, tables, image usage |
| **Keyword Coverage** | 20% | Technical competencies, frameworks, tool platforms, and soft skills |
| **Contact Information** | 15% | Name detection, email, phone number, LinkedIn / GitHub profile links |

> **Important**: All scores and reports are labelled as **ResumeSense-generated compatibility scores**. They simulate real-world parser heuristics and do not guarantee an employer hiring decision.

---

## ⚡ Quick Start

### 1. Run with Docker Compose (Recommended)

Start all services (PostgreSQL, Django backend, and React/Nginx frontend) with one command:

```bash
docker compose up --build
```

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000/api/](http://localhost:8000/api/)
- **PostgreSQL Database**: `localhost:5433` (Docker host port)
- **Admin**: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

### 2. Run Locally for Development

#### Backend Setup

```bash
# 1. From the repo root, copy the single environment template
cp .env.example .env

cd backend

# 2. Activate virtual environment
.\venv\Scripts\activate   # Windows
# source venv/bin/activate # Linux / macOS

# 3. Run migrations
python manage.py migrate

# 4. Seed demo data (Pre-populates Faizan Fatmi demo user & analysis)
python manage.py seed_demo_data

# 5. Start backend server
python manage.py runserver 8000
```

#### Frontend Setup

```bash
cd frontend

# 1. Install dependencies
npm install

# 2. Start Vite development server (proxies /api to the backend automatically)
npm run dev
```

Visit [http://localhost:5173](http://localhost:5173) in your browser.

---

## ☁️ Deploy to Render (single service)

The React frontend is **built into and served by the Django backend**, so the
whole app runs as **one** Render web service — no separate frontend host, no CORS,
no `VITE_API_URL` to manage. A single **`.env` / `.env.example`** at the repo root
configures everything.

The repo ships a **`render.yaml`** Blueprint that provisions it in one step:

1. In Render, choose **New → Blueprint** and select this repository. It creates a
   Postgres database and one **Docker web service** (root `Dockerfile`) that builds
   the frontend and serves the SPA, the `/api` endpoints, and the admin together.
2. `SECRET_KEY`, `JWT_SECRET`, and `DATABASE_URL` are generated / wired
   automatically — nothing to set by hand after the first deploy.

> The backend loads `torch` / `sentence-transformers`, which are memory-hungry.
> The Blueprint defaults to the `standard` instance; the `free` Postgres plan
> expires after 30 days — raise both for real production use.

---

## 🧪 Running Automated Tests

Run backend unit tests verifying authentication, parser rules, scoring heuristics, and job matching:

```bash
cd backend
python manage.py test apps.accounts.tests apps.analysis.tests apps.jobmatcher.tests
```

Build and validate the frontend TypeScript bundle:

```bash
cd frontend
npm run build
```

---

## 🔑 Demo Account Credentials

A pre-populated account is available out of the box:
- **Username**: `faizan`
- **Password**: `ResumeSense123!`
- **Sample File**: `Faizan_Resume.pdf` (Score: **87 / 100**)

You can also click **"Try Sample"** anywhere in the app to instantly test the analysis interface.

---

## 🛡️ Security & Privacy

- All uploaded files are sanitized and validated against allowed binary signatures and extensions.
- Files are protected behind user-level object permissions; users cannot access another user's files or analysis records.
- Environment variables isolate database credentials and secrets.
- JWT tokens expire and rotate automatically.

---

## 📄 License

MIT License. Designed and built for professional career and recruitment analysis.
