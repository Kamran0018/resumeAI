<div align="center">

# 🤖 Resume AI — Intelligent Resume Screening Platform

**An AI-powered Django web application that automates resume screening, candidate-job matching, and recruitment workflows using Google Gemini 2.5 Flash.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.x-green?logo=django)](https://djangoproject.com)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-orange?logo=google)](https://ai.google.dev)
[![SQLite](https://img.shields.io/badge/Database-SQLite3-lightblue?logo=sqlite)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-purple)](LICENSE)

</div>

---

## 📋 Table of Contents

| # | Section |
|---|---------|
| 1 | [Project Title](#1-project-title) |
| 2 | [Project Overview](#2-project-overview) |
| 3 | [Problem Statement](#3-problem-statement) |
| 4 | [Solution](#4-solution) |
| 5 | [Project Objectives](#5-project-objectives) |
| 6 | [Key Features](#6-key-features) |
| 7 | [User Roles](#7-user-roles) |
| 8 | [Complete Workflow](#8-complete-workflow) |
| 9 | [System Architecture](#9-system-architecture) |
| 10 | [AI Workflow](#10-ai-workflow) |
| 11 | [Module-wise Explanation](#11-module-wise-explanation) |
| 12 | [Folder Structure](#12-folder-structure) |
| 13 | [Database Design](#13-database-design) |
| 14 | [Technologies Used](#14-technologies-used) |
| 15 | [Libraries & APIs Used](#15-libraries--apis-used) |
| 16 | [Installation Guide](#16-installation-guide) |
| 17 | [Environment Variables](#17-environment-variables) |
| 18 | [Project Setup Instructions](#18-project-setup-instructions) |
| 19 | [Running the Project](#19-running-the-project) |
| 20 | [Screenshots](#20-screenshots) |
| 21 | [API Integration Details](#21-api-integration-details) |
| 22 | [AI Features](#22-ai-features) |
| 23 | [Resume Parsing Workflow](#23-resume-parsing-workflow) |
| 24 | [Job Description Analysis Workflow](#24-job-description-analysis-workflow) |
| 25 | [AI Resume Analysis](#25-ai-resume-analysis) |
| 26 | [AI Resume Recommendation](#26-ai-resume-recommendation) |
| 27 | [AI Resume Builder](#27-ai-resume-builder) |
| 28 | [AI Voice Assistant](#28-ai-voice-assistant) |
| 29 | [Resume vs Job Description Matching](#29-resume-vs-job-description-matching) |
| 30 | [Recruiter AI Dashboard](#30-recruiter-ai-dashboard) |
| 31 | [Candidate AI Dashboard](#31-candidate-ai-dashboard) |
| 32 | [Candidate Ranking System](#32-candidate-ranking-system) |
| 33 | [AI Recommendation Engine](#33-ai-recommendation-engine) |
| 34 | [Explainable AI Scoring Logic](#34-explainable-ai-scoring-logic) |
| 35 | [Database Models](#35-database-models) |
| 36 | [Security Features](#36-security-features) |
| 37 | [Future Enhancements](#37-future-enhancements) |
| 38 | [Challenges Faced](#38-challenges-faced) |
| 39 | [Project Outcomes](#39-project-outcomes) |
| 40 | [Learning Outcomes](#40-learning-outcomes) |
| 41 | [Deployment Readiness](#41-deployment-readiness) |
| 42 | [Testing Strategy](#42-testing-strategy) |
| 43 | [Performance Optimizations](#43-performance-optimizations) |
| 44 | [License](#44-license) |
| 45 | [Author Information](#45-author-information) |

---

## 1. Project Title

# Resume AI — Intelligent Resume Screening & Candidate Matching Platform

> Automating the recruitment pipeline with Google Gemini AI, natural language understanding, and an end-to-end Django web application.

---

## 2. Project Overview

**Resume AI** is a full-stack web application built with **Django** that bridges the gap between job seekers (candidates) and employers (recruiters) using the power of **Generative AI**. The platform provides:

- **Candidates** with AI-driven resume feedback, score analysis, voice-based coaching, and real-time job matching scores.
- **Recruiters** with AI-powered candidate ranking, application management, and an intelligent dashboard to identify the best-fit candidates instantly.

The AI engine is powered by **Google Gemini 2.5 Flash**, with a rule-based fallback system that ensures the platform remains fully functional even without API access. The platform features automatic resume parsing from PDF and DOCX files, structured data extraction, semantic matching, and text-to-speech voice feedback.

---

## 3. Problem Statement

Traditional recruitment is broken in several ways:

- 📄 **Recruiters receive hundreds of resumes** for a single job posting — manually reviewing all of them is time-consuming and error-prone.
- 🎯 **Candidates don't know why they're rejected** — they receive no actionable feedback on their resumes.
- 🔍 **Keyword-based filtering misses qualified candidates** — simple ATS systems cannot understand context or semantic similarity.
- ⏳ **Time-to-hire is long** — screening, shortlisting, and ranking take days or weeks.
- 🤖 **No personalized guidance** — candidates are left to guess what skills to add or how to improve.

---

## 4. Solution

Resume AI addresses these problems with:

| Problem | Solution |
|---------|----------|
| Manual resume screening | AI-powered candidate ranking with match scores |
| No resume feedback | Gemini AI-generated analysis with strengths, weaknesses & suggestions |
| Poor keyword matching | Semantic + skill + keyword + experience multi-dimensional scoring |
| Slow shortlisting | Instant ranked candidate list on the recruiter dashboard |
| No candidate guidance | AI voice coaching + written recommendations personalized per resume |
| Resume parsing difficulty | Automatic extraction from PDF/DOCX using PyPDF2 + python-docx |

---

## 5. Project Objectives

1. **Automate Resume Screening** — Reduce manual effort in the recruitment process by 80%.
2. **Provide AI-Powered Feedback** — Give candidates actionable, personalized resume improvement advice.
3. **Enable Semantic Job Matching** — Match candidates to jobs beyond simple keyword overlap.
4. **Rank Candidates Intelligently** — Present recruiters with a ranked leaderboard of applicants.
5. **Deliver Voice Coaching** — Convert AI insights into audio feedback using text-to-speech.
6. **Ensure Role-Based Access** — Separate dashboards and permissions for candidates and recruiters.
7. **Build a Scalable Foundation** — Structure the codebase for future enhancements (email verification, notifications, REST API).

---

## 6. Key Features

### For Candidates
- ✅ Upload resumes in PDF, DOCX, DOC, or TXT format (up to 10MB)
- ✅ Automatic parsing: skills, experience, education, and contact info extracted instantly
- ✅ AI-generated resume score (0–100) with detailed breakdown
- ✅ Strengths & weaknesses analysis powered by Gemini AI
- ✅ Actionable improvement suggestions
- ✅ Voice feedback — AI coaching delivered as an MP3 audio file
- ✅ Browse all active job listings
- ✅ Apply for jobs with one click (resume auto-attached)
- ✅ Instant AI match score upon application
- ✅ Application status tracking (Applied → Reviewing → Shortlisted → Interview → Offered/Rejected)
- ✅ Personal dashboard with stats: resumes, skills count, applications, shortlisted count

### For Recruiters
- ✅ Post detailed job listings with type, level, salary, required/preferred skills
- ✅ Manage all posted jobs
- ✅ View ranked candidates per job (AI-sorted by match score)
- ✅ View per-candidate matched and missing skills
- ✅ Update application statuses with recruiter notes
- ✅ Recruiter dashboard: jobs posted, total applications, AI-matched count, average score
- ✅ Resume search by skill/keyword

### Platform
- ✅ Separate login flows for candidates and recruiters
- ✅ Role-based access control on every view
- ✅ Graceful AI fallback (rule-based analysis when Gemini is unavailable)
- ✅ File management with media storage
- ✅ Django Admin panel

---

## 7. User Roles

### Role Comparison Table

| Feature | Candidate | Recruiter | Admin |
|---------|:---------:|:---------:|:-----:|
| Register & Login | ✅ | ✅ | ✅ |
| Upload Resume | ✅ | ❌ | ✅ |
| AI Resume Analysis | ✅ | ❌ | ✅ |
| Voice Feedback | ✅ | ❌ | ✅ |
| Browse Jobs | ✅ | ✅ | ✅ |
| Apply to Jobs | ✅ | ❌ | ❌ |
| View Match Score | ✅ | ❌ | ✅ |
| Track Application Status | ✅ | ❌ | ✅ |
| Post Jobs | ❌ | ✅ | ✅ |
| View All Applications | ❌ | ✅ | ✅ |
| Update Application Status | ❌ | ✅ | ✅ |
| AI Rank Candidates | ❌ | ✅ | ✅ |
| Resume Search | ❌ | ✅ | ✅ |
| Manage All Users | ❌ | ❌ | ✅ |

### Candidate Role
A candidate registers with their email, username, and phone. Upon registration, a `CandidateProfile` is automatically created. They can upload multiple resumes, receive AI feedback on each, and apply to active job postings.

### Recruiter Role
A recruiter registers with company name and position. A `RecruiterProfile` is created. They post jobs, view the AI-ranked candidate list, and move applications through the hiring pipeline.

### Admin Role
Django's built-in superuser with access to the `/admin/` panel. Can manage all users, jobs, resumes, and applications.

---

## 8. Complete Workflow

### Candidate Workflow

```
[Register as Candidate]
        |
        v
[Login with Email + Password]
        |
        v
[Candidate Dashboard]
  - View resume stats
  - View application stats
        |
        v
[Upload Resume (PDF/DOCX/TXT)]
        |
        v
[Automatic Parsing]
  - Skills extracted
  - Experience extracted
  - Education extracted
  - Contact info extracted
        |
        v
[AI Resume Analysis]
  - Score (0-100)
  - Strengths
  - Weaknesses
  - Suggestions
        |
        v
[Voice Feedback Generated (MP3)]
        |
        v
[Browse Active Jobs]
        |
        v
[Apply to Job]
  - Resume auto-attached
  - AI match score calculated instantly
  - Application stored with breakdown
        |
        v
[Track Application Status]
  Applied -> Under Review -> Shortlisted
          -> Interview -> Offered / Rejected
```

### Recruiter Workflow

```
[Register as Recruiter]
        |
        v
[Login with Email + Password]
        |
        v
[Recruiter Dashboard]
  - Jobs posted
  - Total applications
  - AI-matched candidates
  - Average match score
        |
        v
[Post a New Job]
  - Title, Company, Location
  - Job Type, Experience Level
  - Description, Requirements
  - Required & Preferred Skills
  - Salary Range
        |
        v
[View Job Detail]
  - Ranked candidate list (AI-sorted)
  - Matched / Missing skills per candidate
  - Recommendation label
        |
        v
[Update Application Status]
  - Applied -> Reviewing -> Shortlisted
            -> Interview -> Offered / Rejected
  - Add recruiter notes
```

---

## 9. System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        CLIENT BROWSER                        │
│              Django Template Engine (HTML/CSS/JS)            │
└────────────────────────────┬─────────────────────────────────┘
                             │ HTTP Requests
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                        DJANGO WEB SERVER                     │
│                     resume_screener/urls.py                  │
│                                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐  │
│  │ accounts │ │ resumes  │ │   jobs   │ │  applications │  │
│  │  (auth)  │ │ (upload) │ │ (post)   │ │   (apply)     │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────────┘  │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                   ai_services                       │    │
│  │  ┌────────────────┐ ┌────────────┐ ┌────────────┐  │    │
│  │  │GeminiAnalyzer  │ │ResumeJob   │ │  AIVoice   │  │    │
│  │  │(resume score)  │ │Matcher     │ │(pyttsx3)   │  │    │
│  │  └────────────────┘ └────────────┘ └────────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
└────────────────────────────┬─────────────────────────────────┘
                             │
            ┌────────────────┴────────────────┐
            │                                 │
            ▼                                 ▼
┌───────────────────────┐        ┌────────────────────────────┐
│   SQLite3 Database    │        │   Google Gemini 2.5 Flash  │
│   (db.sqlite3)        │        │   (REST API via google-    │
│                       │        │    genai Python package)   │
│  - users              │        └────────────────────────────┘
│  - candidate_profiles │
│  - recruiter_profiles │
│  - resumes            │
│  - jobs               │
│  - applications       │
└───────────────────────┘
```

### Module Dependency Diagram

```
accounts
   └── models.py (User, CandidateProfile, RecruiterProfile)
         ▲
         │ ForeignKey
resumes ─┘
   └── models.py (Resume)
   └── services.py (ResumeParser)
         ▲
         │ ForeignKey
jobs ────┘
   └── models.py (Job)
         ▲
         │ ForeignKey
applications
   └── models.py (Application → User + Job + Resume)
         ▲
         │ Imported by
ai_services
   ├── gemini_analyzer.py
   ├── matcher.py (uses Resume + Job + Application)
   └── voice.py
```

---

## 10. AI Workflow

### AI Pipeline Diagram

```
┌───────────────────────────────────────────────────────────┐
│                    AI PIPELINE                            │
│                                                           │
│  INPUT: Resume Text / Job Description                     │
│         (reconstructed from JSON fields)                  │
│                          │                                │
│                          ▼                                │
│  ┌─────────────────────────────────────────────────────┐ │
│  │              GEMINI 2.5 FLASH LLM                   │ │
│  │                                                     │ │
│  │  Structured Prompt (JSON format enforced)           │ │
│  │  → Resume Analysis:                                 │ │
│  │    score, rating, strengths, weaknesses,            │ │
│  │    suggestions, recommendation, summary             │ │
│  │                                                     │ │
│  │  → Job Match Analysis:                              │ │
│  │    overall_score, skill_match, experience_match,    │ │
│  │    keyword_match, semantic_match,                   │ │
│  │    matched_skills, missing_skills,                  │ │
│  │    recommendation, recommendations, summary         │ │
│  └─────────────────────────────────────────────────────┘ │
│                          │                                │
│              ┌───────────┴───────────┐                   │
│              │  Gemini Available?    │                    │
│              └───────────┬───────────┘                   │
│                  YES ────┘──── NO                        │
│                   │              │                        │
│                   ▼              ▼                        │
│           JSON Response     Rule-Based Fallback           │
│           (parsed from      (skill keyword matching       │
│            LLM output)       + scoring heuristics)        │
│                   │              │                        │
│                   └──────┬───────┘                        │
│                          │                                │
│                          ▼                                │
│              Saved to Database (JSONField)                │
│                          │                                │
│              ┌───────────┴────────────┐                   │
│              │                        │                   │
│              ▼                        ▼                   │
│    Rendered to Template        Voice Synthesis             │
│    (score, feedback,           (pyttsx3 → MP3)            │
│     matched skills)                                       │
└───────────────────────────────────────────────────────────┘
```

---

## 11. Module-wise Explanation

### Module 1: `accounts` — Authentication & User Management

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Manage user registration, login, logout, and profiles for two distinct roles |
| **Input** | Email, username, password, phone (+ company/position for recruiter) |
| **Processing** | Creates a `User` record + role-specific profile (`CandidateProfile` or `RecruiterProfile`) atomically |
| **Output** | Authenticated session, role-based dashboard redirect |
| **Technologies** | Django Auth, `AbstractUser`, Session middleware |

Key components:
- `models.py` — `User` (email-based auth), `CandidateProfile`, `RecruiterProfile`
- `views.py` — `register_candidate`, `register_recruiter`, `login_candidate`, `login_recruiter`, `user_logout`, `profile`
- `serializers.py` — DRF serializers with JWT token generation (foundation for future REST API)
- `permissions.py` — Role-based permission helpers

---

### Module 2: `resumes` — Resume Management & Parsing

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Handle resume uploads, file parsing, and display with AI-generated feedback |
| **Input** | PDF, DOCX, DOC, or TXT file (max 10MB) |
| **Processing** | File stored to `media/resumes/`, then `ResumeParser` extracts structured fields; AI analysis triggered on first view |
| **Output** | Structured resume record (skills, experience, education, contact), AI score and feedback |
| **Technologies** | Django FileField, PyPDF2, python-docx, regex, Gemini AI |

Key components:
- `models.py` — `Resume` model with JSON fields for skills, experience, education
- `services.py` — `ResumeParser` class with PDF/DOCX extraction and keyword-based skill detection
- `views.py` — `upload_resume`, `resume_list`, `resume_detail`, `delete_resume`, `analyze_resume`, `search_resumes`, `dashboard`

---

### Module 3: `jobs` — Job Listings

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Allow recruiters to post jobs and candidates to browse and apply |
| **Input** | Job title, company, location, type, level, description, requirements, skills, salary |
| **Processing** | Job saved to DB; on apply, AI matcher immediately computes match score |
| **Output** | Job listing, ranked candidates on detail view |
| **Technologies** | Django ORM, `ResumeJobMatcher` |

Key components:
- `models.py` — `Job` with job type, experience level, skills (comma-separated), salary range, status flags
- `views.py` — `post_job`, `my_jobs`, `job_detail` (with AI ranking), `all_jobs`, `apply_job`

---

### Module 4: `applications` — Application Lifecycle

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Track candidate applications from submission to final hiring decision |
| **Input** | Candidate + Job + Resume (auto-selected, first resume) |
| **Processing** | Creates `Application` record; AI match score computed and stored; status updated by recruiter |
| **Output** | Application with match score, breakdown, recommendation, and status |
| **Technologies** | Django ORM, `ResumeJobMatcher` |

Key components:
- `models.py` — `Application` with 7 status choices, `match_score`, `match_breakdown` (JSON), `ai_recommendation`, `recruiter_notes`
- `views.py` — `application_detail`, `my_applications`, `all_applications`, `update_status`

---

### Module 5: `ai_services` — AI Engine

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Central AI engine for resume analysis, job matching, candidate ranking, and voice feedback |
| **Input** | Resume text + Job description text |
| **Processing** | Sends structured prompts to Gemini API; parses JSON response; falls back to rule-based logic |
| **Output** | Structured JSON with scores, labels, skill lists, recommendations |
| **Technologies** | `google-genai`, `pyttsx3`, JSON parsing, regex |

Sub-modules:
- `gemini_analyzer.py` — `GeminiAnalyzer` class for resume scoring
- `matcher.py` — `ResumeJobMatcher` class for job matching and bulk ranking
- `voice.py` — `AIVoice` class for text-to-speech MP3 generation
- `views.py` — API endpoints wrapping the AI services

---

## 12. Folder Structure

```
Resume_AI/
│
├── resume_screener/                  # Django project configuration
│   ├── __init__.py
│   ├── settings.py                   # All settings: DB, Auth, Media, Gemini key
│   ├── urls.py                       # Root URL routing (5 app includes)
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                         # User auth & profiles
│   ├── models.py                     # User, CandidateProfile, RecruiterProfile
│   ├── views.py                      # Registration, login, logout, profile
│   ├── urls.py                       # /accounts/* routes
│   ├── serializers.py                # DRF serializers (JWT-ready)
│   ├── permissions.py                # Role-based permission helpers
│   ├── admin.py
│   └── migrations/
│
├── resumes/                          # Resume upload, parsing, AI feedback
│   ├── models.py                     # Resume model (skills/exp/edu as JSON)
│   ├── views.py                      # Upload, list, detail, delete, analyze, search
│   ├── services.py                   # ResumeParser (PDF, DOCX, TXT)
│   ├── urls.py                       # / and /dashboard/ and /upload/ etc.
│   ├── admin.py
│   └── migrations/
│
├── jobs/                             # Job postings management
│   ├── models.py                     # Job model (type, level, skills, salary)
│   ├── views.py                      # post_job, my_jobs, job_detail, apply_job
│   ├── urls.py                       # /jobs/* routes
│   ├── admin.py
│   └── migrations/
│
├── applications/                     # Job application tracking
│   ├── models.py                     # Application (match_score, status, breakdown)
│   ├── views.py                      # Detail, list, update status
│   ├── urls.py                       # /applications/* routes
│   ├── admin.py
│   └── migrations/
│
├── ai_services/                      # Core AI engine
│   ├── __init__.py                   # Package-level imports
│   ├── gemini_analyzer.py            # GeminiAnalyzer: resume scoring via Gemini
│   ├── matcher.py                    # ResumeJobMatcher: matching + ranking
│   ├── voice.py                      # AIVoice: text-to-speech MP3
│   ├── views.py                      # AI API endpoints (analyze, match, rank, voice)
│   ├── urls.py                       # /ai/* routes
│   ├── admin.py
│   └── migrations/
│
├── notifications/                    # (Foundation module, future use)
│   ├── models.py
│   └── views.py
│
├── candidates/                       # (Foundation module, future use)
├── recruiters/                       # (Foundation module, future use)
│
├── templates/                        # HTML templates
│   ├── base.html                     # Global layout (nav, footer, CSS vars)
│   ├── home.html                     # Landing page
│   ├── accounts/
│   │   ├── login_candidate.html
│   │   ├── login_recruiter.html
│   │   ├── register_candidate.html
│   │   ├── register_recruiter.html
│   │   └── profile.html
│   ├── candidate/
│   │   └── dashboard.html            # Candidate dashboard
│   ├── recruiter/
│   │   └── dashboard.html            # Recruiter AI dashboard
│   ├── jobs/
│   │   ├── post_job.html
│   │   ├── my_jobs.html
│   │   ├── all_jobs.html
│   │   └── job_detail.html
│   ├── resumes/
│   │   ├── upload.html
│   │   ├── list.html
│   │   └── detail.html
│   └── applications/
│       ├── my_applications.html
│       ├── all_applications.html
│       └── application_detail.html
│
├── media/                            # Uploaded files (gitignored)
│   ├── resumes/                      # Uploaded resume files
│   ├── profiles/                     # Profile pictures
│   └── voice/                        # Generated MP3 audio files
│
├── static/                           # Static assets
├── venv/                             # Virtual environment (gitignored)
├── db.sqlite3                        # SQLite database
├── manage.py
├── .env                              # Environment variables (gitignored)
└── README.md
```

---

## 13. Database Design

### Entity-Relationship Overview

```
┌──────────────────────────────────────────────────────────────┐
│  users                                                       │
│  ─────────────────────────────────────────────────────────   │
│  id (PK) | email (UNIQUE) | username | password | user_type  │
│  phone | profile_picture | is_verified | email_verified      │
│  created_at | updated_at                                      │
└──────────┬────────────────────────────┬─────────────────────┘
           │ 1:1                        │ 1:1
           ▼                            ▼
┌──────────────────────┐  ┌──────────────────────────────────┐
│  candidate_profiles  │  │  recruiter_profiles              │
│  ────────────────    │  │  ───────────────────────────     │
│  user (FK, 1:1)      │  │  user (FK, 1:1)                  │
│  first_name          │  │  company | company_website       │
│  last_name | title   │  │  position | department           │
│  location | about    │  │  company_description | verified  │
│  skills (JSON)       │  │  created_at | updated_at         │
│  experience_years    │  └──────────────────────────────────┘
│  education (JSON)    │
└──────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  resumes                                                │
│  ─────────────────────────────────────────────────────  │
│  id (PK) | user (FK → users) | title | file            │
│  skills (JSON) | experience (JSON) | education (JSON)  │
│  contact_info (JSON) | ai_suggestions (JSON)           │
│  created_at                                            │
└─────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  jobs                                                        │
│  ──────────────────────────────────────────────────────────  │
│  id (PK) | recruiter (FK → users) | title | company         │
│  location | job_type | experience_level                     │
│  description | responsibilities | requirements              │
│  preferred_qualifications | benefits                        │
│  required_skills (text) | preferred_skills (text)           │
│  salary_min | salary_max | currency                         │
│  is_active | is_featured | application_deadline             │
│  views_count | applications_count                           │
│  created_at | updated_at                                    │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  applications                                                │
│  ──────────────────────────────────────────────────────────  │
│  id (PK) | candidate (FK → users) | job (FK → jobs)         │
│  resume (FK → resumes, nullable)                            │
│  match_score (float) | match_breakdown (JSON)               │
│  ai_recommendation (char) | status (char, 7 choices)        │
│  recruiter_notes (text)                                     │
│  applied_at | updated_at                                    │
│  UNIQUE: (candidate, job)                                   │
│  ORDERING: -match_score, -applied_at                       │
└──────────────────────────────────────────────────────────────┘
```

### Application Status State Machine

```
[Applied] ──► [Under Review] ──► [Shortlisted] ──► [Interview] ──► [Offered]
                                        │                               │
                                        └───────────────────────────────►[Rejected]
                                        
[Any State] ──► [Withdrawn]
```

---

## 14. Technologies Used

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Language** | Python | 3.10+ | Backend logic |
| **Web Framework** | Django | 4.x | MVC web framework |
| **AI / LLM** | Google Gemini | 2.5 Flash | Resume analysis, matching |
| **AI SDK** | google-genai | Latest | Python client for Gemini API |
| **TTS** | pyttsx3 | Latest | Text-to-speech voice feedback |
| **PDF Parsing** | PyPDF2 | Latest | Extract text from PDF resumes |
| **DOCX Parsing** | python-docx | Latest | Extract text from DOCX resumes |
| **Database** | SQLite3 | Built-in | Development database |
| **ORM** | Django ORM | Built-in | Database abstraction |
| **Auth** | Django Auth | Built-in | Session-based authentication |
| **REST (partial)** | djangorestframework | Latest | Serializers (JWT-ready) |
| **JWT** | djangorestframework-simplejwt | Latest | Token infrastructure |
| **Config** | python-dotenv | Latest | `.env` file loading |
| **Image** | Pillow | Latest | Profile picture handling |
| **Templating** | Django Templates | Built-in | Server-side HTML rendering |
| **Frontend** | HTML5 / CSS3 / JS | - | UI |

---

## 15. Libraries & APIs Used

### Python Libraries

| Library | Purpose |
|---------|---------|
| `google.genai` | Official Python client for Google Gemini API |
| `PyPDF2` | Extract raw text from PDF resume files |
| `python-docx` | Extract text from DOCX resume files |
| `pyttsx3` | Offline text-to-speech engine for voice feedback |
| `python-dotenv` | Load environment variables from `.env` |
| `Pillow` | Image processing for profile pictures |
| `djangorestframework` | Serialization layer (JWT-ready API foundation) |
| `djangorestframework-simplejwt` | JWT token generation infrastructure |
| `re` (stdlib) | Regular expressions for resume parsing |
| `json` (stdlib) | Parse Gemini API JSON responses |
| `os` (stdlib) | File path operations |

### External APIs

| API | Provider | Usage |
|-----|----------|-------|
| **Gemini API** | Google AI Studio | Resume analysis + job matching prompts |
| Model: `gemini-2.5-flash` | Google DeepMind | Fast, cost-effective LLM inference |

### API Integration Pattern

```python
# Initialize client
from google import genai
client = genai.Client(api_key=settings.GEMINI_API_KEY)

# Send structured prompt
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt
)

# Parse JSON from response
text = response.text
json_str = text[text.find('{') : text.rfind('}') + 1]
result = json.loads(json_str)
```

---

## 16. Installation Guide

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.10 or higher |
| pip | Latest |
| Git | Any |
| Google Gemini API Key | Free at [aistudio.google.com](https://aistudio.google.com/app/apikey) |

### Step-by-Step Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/Resume_AI.git
cd Resume_AI

# 2. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install all dependencies
pip install django python-dotenv google-genai pyttsx3 PyPDF2 python-docx Pillow djangorestframework djangorestframework-simplejwt

# 4. Create .env file (see Section 17)

# 5. Run database migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create required directories
mkdir -p media/resumes media/profiles media/voice static staticfiles

# 7. Create admin superuser (optional)
python manage.py createsuperuser

# 8. Start development server
python manage.py runserver
```

---

## 17. Environment Variables

Create a `.env` file in the project root with the following contents:

```env
# =============================================
# GOOGLE GEMINI AI
# =============================================
GEMINI_API_KEY=your_gemini_api_key_here

# =============================================
# DJANGO SETTINGS
# =============================================
DEBUG=True
SECRET_KEY=your-very-long-secret-key-here-replace-this

# =============================================
# DATABASE (optional — defaults to SQLite)
# =============================================
# DATABASE_URL=postgres://user:password@localhost:5432/resume_ai
```

> **Security Warning:** Never commit your `.env` file. Add it to `.gitignore` immediately.

### Getting a Gemini API Key

1. Visit [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key and paste it as `GEMINI_API_KEY` in `.env`

---

## 18. Project Setup Instructions

```bash
# Full setup from scratch

# Clone
git clone https://github.com/your-username/Resume_AI.git
cd Resume_AI

# Virtual environment
python -m venv venv
venv\Scripts\activate           # Windows
# source venv/bin/activate      # Linux/Mac

# Install dependencies
pip install -r requirements.txt
# OR manually:
pip install django==4.2 python-dotenv google-genai pyttsx3 PyPDF2 python-docx Pillow djangorestframework djangorestframework-simplejwt

# Environment
copy .env.example .env         # Windows
# cp .env.example .env         # Linux/Mac
# Edit .env with your API keys

# Database
python manage.py makemigrations accounts resumes jobs applications ai_services
python manage.py migrate

# Static files (optional)
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Run
python manage.py runserver
```

### Generate requirements.txt

```bash
pip freeze > requirements.txt
```

---

## 19. Running the Project

```bash
# Development server (default: http://127.0.0.1:8000/)
python manage.py runserver

# Custom port
python manage.py runserver 8080

# Accessible on network
python manage.py runserver 0.0.0.0:8000
```

### Key URLs

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Home / Landing page |
| `http://127.0.0.1:8000/dashboard/` | Role-based dashboard (login required) |
| `http://127.0.0.1:8000/accounts/login/candidate/` | Candidate login |
| `http://127.0.0.1:8000/accounts/login/recruiter/` | Recruiter login |
| `http://127.0.0.1:8000/accounts/register/candidate/` | Candidate registration |
| `http://127.0.0.1:8000/accounts/register/recruiter/` | Recruiter registration |
| `http://127.0.0.1:8000/upload/` | Upload resume |
| `http://127.0.0.1:8000/jobs/all/` | Browse all jobs |
| `http://127.0.0.1:8000/jobs/post/` | Post a job (recruiter only) |
| `http://127.0.0.1:8000/admin/` | Django admin panel |

---

## 20. Screenshots

> **Note:** Screenshots are placeholders — replace with actual project screenshots.

### Landing Page
```
┌────────────────────────────────────────────────────────────┐
│  🤖 Resume AI                            [Login] [Register]│
│                                                            │
│    Intelligent Resume Screening Platform                   │
│    Powered by Google Gemini AI                             │
│                                                            │
│    [Register as Candidate]   [Register as Recruiter]       │
└────────────────────────────────────────────────────────────┘
```

### Candidate Dashboard
```
┌────────────────────────────────────────────────────────────┐
│  My Dashboard                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │
│  │Resumes: 2│ │Skills: 12│ │Applied: 5│ │Shortlisted: 1│ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │
│                                                            │
│  Recent Resumes                    Recent Applications     │
│  ├─ My Resume v2   Score: 82/100   ├─ Google    Applied   │
│  └─ Internship CV  Score: 67/100   └─ Microsoft Reviewing │
└────────────────────────────────────────────────────────────┘
```

### Recruiter AI Dashboard
```
┌────────────────────────────────────────────────────────────┐
│  Recruiter Dashboard                                       │
│  ┌───────────┐ ┌──────────────┐ ┌──────────┐ ┌─────────┐ │
│  │Jobs: 3    │ │Applications:8│ │Matched: 5│ │Avg: 74% │ │
│  └───────────┘ └──────────────┘ └──────────┘ └─────────┘ │
│                                                            │
│  AI-Ranked Candidates                                      │
│  #1 Alice Smith  95%  ✅Python ✅Django ❌AWS              │
│  #2 Bob Jones    81%  ✅Python ❌Docker ❌Kubernetes       │
│  #3 Carol Lee    67%  ✅SQL    ❌React  ❌Node.js          │
└────────────────────────────────────────────────────────────┘
```

---

## 21. API Integration Details

### Gemini API — Resume Analysis

**Endpoint:** `POST` via `google-genai` SDK  
**Model:** `gemini-2.5-flash`  
**Input limit:** 5,000 characters of resume text

**Request Prompt Structure:**
```python
prompt = f"""
You are an expert resume coach. Analyze this resume and give detailed feedback.

RESUME:
{resume_text[:5000]}

Give me a detailed analysis in this EXACT JSON format. No extra text, only JSON:
{{
    "score": 75,
    "rating": "Good",
    "strengths": ["..."],
    "weaknesses": ["..."],
    "suggestions": ["..."],
    "recommendation": "...",
    "summary": "..."
}}
"""
```

**Response JSON Schema:**
```json
{
  "score": "integer (0-100)",
  "rating": "string (Poor/Average/Good/Excellent)",
  "strengths": ["string"],
  "weaknesses": ["string"],
  "suggestions": ["string"],
  "recommendation": "string",
  "summary": "string"
}
```

### Gemini API — Job Matching

**Request Prompt Structure:**
```python
prompt = f"""
You are an expert recruiter. Analyze this resume against the job description.

JOB DESCRIPTION:
{job_text}

RESUME:
{resume_text[:5000]}

Give me a match analysis in this EXACT JSON format:
{{
    "overall_score": 85,
    "skill_match": 90,
    "experience_match": 80,
    "keyword_match": 85,
    "semantic_match": 75,
    "matched_skills": ["..."],
    "missing_skills": ["..."],
    "recommendation": "...",
    "recommendations": ["..."],
    "summary": "..."
}}
"""
```

**Response JSON Schema:**
```json
{
  "overall_score": "float (0-100)",
  "skill_match": "float (0-100)",
  "experience_match": "float (0-100)",
  "keyword_match": "float (0-100)",
  "semantic_match": "float (0-100)",
  "matched_skills": ["string"],
  "missing_skills": ["string"],
  "recommendation": "string",
  "recommendations": ["string"],
  "summary": "string"
}
```

### Error Handling & Fallback

```
Gemini API Call
    │
    ├── Success ──► Parse JSON ──► Return result
    │
    └── Exception ──► Rule-based fallback
                           │
                           ├── Skill keyword matching
                           ├── Count-based scoring
                           └── Static recommendations
```

---

## 22. AI Features

| Feature | Status | Engine | Description |
|---------|--------|--------|-------------|
| Resume Scoring | ✅ Implemented | Gemini 2.5 Flash + Fallback | 0-100 score with rating |
| Strength Detection | ✅ Implemented | Gemini 2.5 Flash | Lists resume strengths |
| Weakness Detection | ✅ Implemented | Gemini 2.5 Flash | Lists areas to improve |
| Improvement Suggestions | ✅ Implemented | Gemini 2.5 Flash | Actionable bullet points |
| Job Matching | ✅ Implemented | Gemini 2.5 Flash + Fallback | Multi-dimensional match |
| Skill Gap Analysis | ✅ Implemented | Gemini 2.5 Flash | Missing skills per job |
| Candidate Ranking | ✅ Implemented | Gemini 2.5 Flash | Sorted by match score |
| Voice Feedback | ✅ Implemented | pyttsx3 | MP3 audio coaching |
| Resume Parsing | ✅ Implemented | PyPDF2 + python-docx | PDF/DOCX extraction |
| Resume Builder | 🚧 Planned | - | AI-assisted resume creation |
| Email Notifications | 🚧 Planned | - | Status change alerts |
| Cover Letter Generator | 🚧 Planned | Gemini | AI-written cover letters |

---

## 23. Resume Parsing Workflow

```
User uploads file (PDF / DOCX / DOC / TXT)
             │
             ▼
    File size validation (≤ 10MB)
    File type validation
             │
             ▼
    Saved to media/resumes/ via Django FileField
             │
             ▼
    ResumeParser.parse(file_path)
             │
      ┌──────┴──────┐
      │ File type?  │
      ├─────────────┤
   .pdf    .docx    .txt/.doc
      │       │         │
   PyPDF2  python-docx  open()
  reader    Document   read()
      │       │         │
      └───────┴─────────┘
             │
      Raw text extracted
             │
             ▼
    _extract_structured_data(text)
             │
      ┌──────┴──────────────────────────────┐
      │                                     │
   Skills extraction            Experience extraction
   (40+ keyword matching)       (job title pattern matching +
      │                          year extraction)
      │                                     │
   Education extraction         Contact info extraction
   (degree keyword matching)    (email regex + phone regex)
             │
             ▼
    {
      'skills': [...],
      'experience': [...],
      'education': [...],
      'contact_info': {...}
    }
             │
             ▼
    Saved to Resume model (JSON fields)
```

**Supported Skills (partial list):** Python, JavaScript, Java, C++, React, Node.js, Django, Flask, SQL, MongoDB, AWS, Docker, Kubernetes, Git, Machine Learning, Data Science, HTML, CSS, PHP, TypeScript, Angular, Vue.js, PostgreSQL, Redis, and 20+ more.

---

## 24. Job Description Analysis Workflow

```
Recruiter creates job posting
             │
             ▼
    Job stored in DB:
    - title, company, location
    - job_type, experience_level
    - description, requirements
    - required_skills (comma-separated)
    - preferred_skills (comma-separated)
             │
             ▼
    Candidate applies to job
             │
             ▼
    ResumeJobMatcher.match(resume, job)
             │
             ▼
    job_text constructed:
    "Title: ... Company: ... Description: ...
     Requirements: ... Required Skills: ..."
             │
             ▼
    Gemini API called with (resume_text + job_text)
             │
             ▼
    Multi-dimensional analysis returned:
    - Overall match score
    - Skill match %
    - Experience match %
    - Keyword match %
    - Semantic match %
    - Matched skills list
    - Missing skills list
             │
             ▼
    Stored in Application.match_breakdown (JSON)
    Application.match_score = overall_score
    Application.ai_recommendation = recommendation
```

---

## 25. AI Resume Analysis

**Implementation:** `GeminiAnalyzer.analyze_resume(resume_text)`

### Processing Steps:

1. **Text Reconstruction** — Joins skills list + experience roles/companies/descriptions + education degrees/institutions into a single text blob.
2. **Prompt Engineering** — Wraps text in a structured Gemini prompt with strict JSON output format.
3. **API Call** — Sends to `gemini-2.5-flash` via `google-genai` SDK.
4. **JSON Extraction** — Uses `text.find('{')` and `text.rfind('}')` to extract clean JSON from response.
5. **Fallback** — If API fails, rule-based `_fallback_analysis()` returns a static structure.
6. **Storage** — Result saved to `Resume.ai_suggestions` (JSONField).
7. **Display** — Rendered in `resumes/detail.html` with score gauge, strengths/weaknesses lists.

### Scoring Rubric (Rule-Based Fallback)

| Component | Max Points | Logic |
|-----------|-----------|-------|
| Skills | 30 | 8+ skills → 30, 5+ → 20, 3+ → 10 |
| Experience | 30 | 3+ entries → 30, 2 → 20, 1 → 10 |
| Education | 20 | 2+ entries → 20, 1 → 10 |
| Email present | 10 | Binary |
| Phone present | 10 | Binary |
| **Total** | **100** | |

---

## 26. AI Resume Recommendation

The AI recommendation system provides personalized, actionable feedback in three layers:

### Layer 1: Gemini AI Recommendations (Primary)
- Generated by the LLM with deep semantic understanding
- Includes specific skill names, technology suggestions, and career advice
- Contextual to the actual resume content

### Layer 2: Rule-Based Recommendations (Fallback)
Triggered when Gemini is unavailable:
```
- "Add numbers to your achievements (e.g., 'Increased sales by 30%')"
- "Learn AWS or Azure to boost your profile"
- "Add a professional summary at the top"
- "Use stronger action verbs like Led, Managed, Developed"
```

### Layer 3: Section-Level Feedback (`generate_ai_feedback` in resumes/views.py)
Per-section analysis with emoji indicators:
- `✅` — Strength identified
- `💡` — Improvement suggestion
- `⚠️` — Warning / missing section

---

## 27. AI Resume Builder

> **Status: 🚧 Planned (Future Enhancement)**

The AI Resume Builder is planned as a future module where:
- Candidates input their experience, education, and skills through a form
- Gemini AI generates a professionally formatted resume draft
- Candidates can download as PDF
- AI suggests improvements in real-time

**Planned Implementation:** New `resume_builder/` Django app with Gemini prompt engineering for structured resume generation.

---

## 28. AI Voice Assistant

**Implementation:** `AIVoice` class in `ai_services/voice.py`

### How It Works

```
AI Analysis Result (JSON dict)
             │
             ▼
    speak_suggestions(analysis)
    or
    speak_match(match_result)
             │
             ▼
    Human-readable script generated:
    "Hello! Here is your resume analysis.
     Your resume score is {score} out of 100.
     Your strengths are: {strengths}
     Areas to improve: {weaknesses}
     My suggestions: {suggestions}
     {summary}"
             │
             ▼
    pyttsx3 engine initialized
    - Rate: 150 words/min
    - Volume: 0.9
             │
             ▼
    save_to_file(text, filename)
    → Saved to: media/voice/resume_{id}_feedback.mp3
    → Returns: /media/voice/resume_{id}_feedback.mp3
             │
             ▼
    JsonResponse({'audio_url': url})
             │
             ▼
    Frontend plays audio in browser
    (HTML5 <audio> tag or JS Audio API)
```

### Voice API Endpoints

| URL | Purpose |
|-----|---------|
| `GET /ai/voice/<resume_id>/` | Generate resume feedback audio |
| `GET /ai/voice-match/<job_id>/` | Generate job match feedback audio |

### Fallback
If `pyttsx3` is unavailable (e.g., headless server), the browser Speech Synthesis API can be used as a client-side fallback.

---

## 29. Resume vs Job Description Matching

**Implementation:** `ResumeJobMatcher.match(resume, job)` in `ai_services/matcher.py`

### Matching Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| `skill_match` | Primary | % of required skills found in resume |
| `experience_match` | Secondary | Experience level alignment |
| `keyword_match` | Secondary | Raw keyword overlap |
| `semantic_match` | Secondary | Contextual/semantic similarity (Gemini) |
| `overall_score` | Final | Weighted aggregate (Gemini-computed) |

### Rule-Based Fallback Matching

When Gemini is unavailable:

```python
resume_skills = [s.lower() for s in resume.skills]
job_skills = [s.lower() for s in job.get_required_skills_list()]

matched = [s for s in job_skills if s in resume_skills]
score = (len(matched) / len(job_skills)) * 100 if job_skills else 50

recommendation = "Recommended" if score >= 60 else "Consider"
```

### Recommendation Labels

| Score Range | Gemini Label |
|-------------|-------------|
| 80–100 | Highly Recommended |
| 60–79 | Recommended |
| 40–59 | Consider |
| 0–39 | Not Recommended |

---

## 30. Recruiter AI Dashboard

**View:** `dashboard()` in `resumes/views.py` (recruiter branch)

### Dashboard Metrics

| Metric | Source |
|--------|--------|
| Jobs Posted | `Job.objects.filter(recruiter=user, is_active=True).count()` |
| Total Applications | `Application.objects.filter(job__in=jobs).count()` |
| AI-Matched (≥70%) | `Application.objects.filter(match_score__gte=70).count()` |
| Average Match Score | `Application.objects.aggregate(avg=Avg('match_score'))` |
| Shortlisted | `Application.objects.filter(status='shortlisted').count()` |
| Top Candidates | Candidates with `score >= 80` |

### AI Candidate Table (per job)

For each active job, the recruiter sees:
- Rank (1, 2, 3, ...)
- Candidate name & email
- AI match score (%)
- Matched skills ✅
- Missing skills ❌
- AI recommendation label
- Current status
- Applied date

Candidates are sorted globally by match score descending using `rank_candidates()`.

---

## 31. Candidate AI Dashboard

**View:** `dashboard()` in `resumes/views.py` (candidate branch)

### Dashboard Metrics

| Metric | Source |
|--------|--------|
| Total Resumes | `Resume.objects.filter(user=user).count()` |
| Total Skills | Sum of `len(resume.skills)` across all resumes |
| Total Applications | `Application.objects.filter(candidate=user).count()` |
| Shortlisted | `Application.objects.filter(status='shortlisted').count()` |
| Interviewing | `Application.objects.filter(status='interview').count()` |
| Recent Resumes | Last 5 resumes |
| Recent Applications | Last 3 applications |

### Candidate Journey on Dashboard

1. **Upload Resume** → Auto-parsed → Skills detected
2. **View Resume Detail** → AI score + feedback displayed
3. **Browse Jobs** → See all active listings
4. **Apply** → Instant AI match score shown in success message
5. **Track Applications** → Status column updated by recruiter

---

## 32. Candidate Ranking System

**Implementation:** `ResumeJobMatcher.rank_candidates(job, applications)` in `ai_services/matcher.py`

### Algorithm

```python
def rank_candidates(self, job, applications):
    ranked = []
    
    for app in applications:
        if app.resume:
            # Run AI matching for each candidate
            result = self.match(app.resume, job)
            ranked.append({
                'application': app,
                'score': result['overall_score'],
                'recommendation': result['recommendation'],
                'matched_skills': result['matched_skills'],
                'missing_skills': result['missing_skills'],
                'skill_match': result['skill_match'],
                'experience_match': result['experience_match'],
            })
    
    # Sort by score descending
    ranked.sort(key=lambda x: x['score'], reverse=True)
    
    # Assign ranks 1, 2, 3, ...
    for i, item in enumerate(ranked, 1):
        item['rank'] = i
    
    return ranked
```

### Where Ranking Is Used

| Location | Context |
|----------|---------|
| `jobs/views.py:job_detail()` | Recruiter views ranked candidates for a specific job |
| `resumes/views.py:dashboard()` | Recruiter dashboard shows top-ranked candidates across all jobs |
| `ai_services/views.py:rank_candidates()` | REST API endpoint returning ranked candidates as JSON |

---

## 33. AI Recommendation Engine

The recommendation engine operates at two levels:

### Resume-Level Recommendations

```
Resume uploaded
      │
      ▼
GeminiAnalyzer.analyze_resume(text)
      │
      ▼
Returns:
  - "suggestions": ["Add AWS skills", "Quantify achievements", ...]
  - "recommendation": "Highly Recommended / Consider / ..."
  - Stored in Resume.ai_suggestions
```

### Job-Match-Level Recommendations

```
Candidate applies to job
      │
      ▼
ResumeJobMatcher.match(resume, job)
      │
      ▼
Returns:
  - "recommendations": ["Learn Docker", "Get AWS certification", ...]
  - "missing_skills": ["AWS", "Docker", "Kubernetes"]
  - "recommendation": label
  - Stored in Application.match_breakdown + Application.ai_recommendation
```

---

## 34. Explainable AI Scoring Logic

The platform is designed for **explainability** — every score is backed by reasoning:

### Resume Score Transparency

```
Score: 82/100
├── Strengths:
│   ✅ 12 skills detected (Python, Django, SQL, React, ...)
│   ✅ 3 experience entries found
│   ✅ Education details present
│
├── Weaknesses:
│   ❌ No quantifiable achievements
│   ❌ Missing cloud skills (AWS, Azure)
│
└── Suggestions:
    💡 Add "Increased performance by X%" style metrics
    💡 Consider AWS certification
    💡 Add a professional summary section
```

### Match Score Transparency

```
Overall Match: 78%
├── Skill Match:      90%  (9/10 required skills present)
├── Experience Match: 70%  (3 years, job requires 2-4)
├── Keyword Match:    80%  (8/10 job keywords found)
├── Semantic Match:   72%  (Gemini contextual analysis)
│
├── ✅ Matched Skills: Python, Django, SQL, React, Git, Docker, MongoDB, Agile, REST API
└── ❌ Missing Skills: Kubernetes, GraphQL
```

---

## 35. Database Models

### `accounts.User` (Custom AbstractUser)

```python
class User(AbstractUser):
    USER_TYPES = [('candidate', 'Candidate'), ('recruiter', 'Recruiter')]
    email          = EmailField(unique=True)          # Login field
    user_type      = CharField(choices=USER_TYPES)
    phone          = CharField(max_length=15)
    profile_picture = ImageField(upload_to='profiles/')
    is_verified    = BooleanField(default=False)
    email_verified = BooleanField(default=False)
    USERNAME_FIELD = 'email'
```

### `accounts.CandidateProfile`

```python
class CandidateProfile(models.Model):
    user              = OneToOneField(User, related_name='candidate_profile')
    first_name        = CharField(max_length=100)
    last_name         = CharField(max_length=100)
    title             = CharField(max_length=200)         # Job title
    location          = CharField(max_length=200)
    about             = TextField()
    skills            = JSONField(default=list)
    experience_years  = FloatField(default=0)
    education         = JSONField(default=list)
```

### `accounts.RecruiterProfile`

```python
class RecruiterProfile(models.Model):
    user                = OneToOneField(User, related_name='recruiter_profile')
    company             = CharField(max_length=200)
    company_website     = URLField()
    position            = CharField(max_length=200)
    department          = CharField(max_length=200)
    company_description = TextField()
    verified            = BooleanField(default=False)
```

### `resumes.Resume`

```python
class Resume(models.Model):
    user         = ForeignKey(User, related_name='resumes')
    title        = CharField(max_length=200, default='My Resume')
    file         = FileField(upload_to='resumes/')
    skills       = JSONField(default=list)           # ["Python", "Django", ...]
    experience   = JSONField(default=list)           # [{"role": ..., "company": ...}]
    education    = JSONField(default=list)           # [{"degree": ..., "institution": ...}]
    contact_info = JSONField(default=dict)           # {"email": ..., "phone": ...}
    ai_suggestions = JSONField(default=list)         # Gemini analysis result
    created_at   = DateTimeField(auto_now_add=True)
```

### `jobs.Job`

```python
class Job(models.Model):
    JOB_TYPES = [full_time, part_time, contract, internship, remote, hybrid]
    EXPERIENCE_LEVELS = [entry, junior, mid, senior, lead, manager]
    
    recruiter         = ForeignKey(User, related_name='posted_jobs')
    title             = CharField(max_length=200)
    company           = CharField(max_length=200)
    location          = CharField(max_length=200)
    job_type          = CharField(choices=JOB_TYPES)
    experience_level  = CharField(choices=EXPERIENCE_LEVELS)
    description       = TextField()
    responsibilities  = TextField()
    requirements      = TextField()
    required_skills   = TextField()           # Comma-separated
    preferred_skills  = TextField()           # Comma-separated
    salary_min/max    = DecimalField()
    is_active         = BooleanField(default=True)
    is_featured       = BooleanField(default=False)
    views_count       = IntegerField(default=0)
    applications_count = IntegerField(default=0)
```

### `applications.Application`

```python
class Application(models.Model):
    STATUS_CHOICES = [applied, reviewing, shortlisted, interview, offered, rejected, withdrawn]
    
    candidate         = ForeignKey(User, related_name='applications')
    job               = ForeignKey(Job, related_name='applications')
    resume            = ForeignKey(Resume, on_delete=SET_NULL, null=True)
    match_score       = FloatField(default=0)            # AI overall score
    match_breakdown   = JSONField(default=dict)          # Full Gemini analysis
    ai_recommendation = CharField(max_length=50)         # "Highly Recommended", etc.
    status            = CharField(choices=STATUS_CHOICES)
    recruiter_notes   = TextField()
    
    class Meta:
        ordering = ['-match_score', '-applied_at']
        unique_together = ['candidate', 'job']
```

---

## 36. Security Features

| Feature | Implementation |
|---------|---------------|
| **CSRF Protection** | Django's `CsrfViewMiddleware` on all POST forms |
| **Password Hashing** | Django's PBKDF2-SHA256 hasher (default) |
| **Password Validation** | Length, common passwords, similarity, numeric checks |
| **Email Uniqueness** | Enforced at DB level (`unique=True`) |
| **Username Uniqueness** | Enforced at DB level |
| **Login Required** | `@login_required` decorator on all protected views |
| **Role-Based Access** | `user_type` check on every recruiter/candidate-specific view |
| **Object-Level Auth** | Ownership check before showing/editing any resource |
| **File Validation** | Extension whitelist (`.pdf`, `.docx`, `.doc`, `.txt`) + size limit (10MB) |
| **Secrets in .env** | API keys and `SECRET_KEY` stored in environment variables, not source code |
| **X-Frame-Options** | `XFrameOptionsMiddleware` prevents clickjacking |
| **Session Security** | Django session middleware with DB-backed sessions |

---

## 37. Future Enhancements

| Feature | Priority | Description |
|---------|----------|-------------|
| **Email Notifications** | High | Send status-change emails to candidates |
| **AI Resume Builder** | High | Generate resumes from form input using Gemini |
| **Cover Letter Generator** | Medium | AI-written cover letters tailored to job |
| **PostgreSQL Migration** | Medium | Switch from SQLite to PostgreSQL for production |
| **REST API** | Medium | Full DRF API with JWT authentication (serializers already exist) |
| **Advanced Filtering** | Medium | Filter jobs by salary, location, experience level |
| **Resume Version Control** | Medium | Track changes across multiple resume versions |
| **Interview Prep AI** | Medium | Gemini-generated practice interview questions per job |
| **LinkedIn Import** | Low | Import candidate data from LinkedIn |
| **Analytics Dashboard** | Low | Charts for application trends and skill demand |
| **Mobile App** | Low | React Native or Flutter mobile client |
| **Multi-language** | Low | Support resumes in languages other than English |
| **Recruiter Verification** | Low | Email-verify recruiter company domains |

---

## 38. Challenges Faced

| Challenge | Solution |
|-----------|---------|
| **Gemini API JSON parsing** | LLM responses include markdown code fences; used `text.find('{')` + `text.rfind('}')` to extract clean JSON |
| **Resume text reconstruction** | Resume text is stored as JSON fields, not raw text; reconstructed by joining skills + experience + education fields |
| **File parsing reliability** | PyPDF2 can fail on scanned PDFs; wrapped in try/except with graceful warning to user |
| **Rule-based fallback accuracy** | Skill keyword matching is case-insensitive and covers 40+ technologies to improve reliability |
| **AI response consistency** | Enforced strict JSON schema in prompt to prevent free-form text responses |
| **Role separation** | Implemented `user_type` checks in every view + redirect logic to keep roles fully isolated |
| **Voice on servers** | pyttsx3 requires audio drivers; documented browser Speech API as client-side fallback |
| **Candidate ranking performance** | For large numbers of applications, each calls Gemini; mitigated by storing `match_score` in DB to avoid re-computation |

---

## 39. Project Outcomes

- ✅ **End-to-end recruitment platform** covering the full hiring lifecycle
- ✅ **AI-powered candidate scoring** with multi-dimensional analysis
- ✅ **Automated resume parsing** from PDF and DOCX with 40+ skill detectors
- ✅ **Voice feedback system** delivering personalized audio coaching
- ✅ **Role-isolated dashboards** with real-time AI metrics for both roles
- ✅ **Scalable codebase** with modular Django apps and a clear extension path
- ✅ **Robust fallback system** ensuring 100% uptime even without API access
- ✅ **REST API foundation** (serializers + JWT) ready for frontend framework integration

---

## 40. Learning Outcomes

1. **LLM Prompt Engineering** — Designing structured prompts that enforce JSON output from Gemini
2. **Django Architecture** — Multi-app Django project with clean separation of concerns
3. **AI Fallback Design** — Building resilient systems with rule-based fallbacks for LLM failure
4. **Resume NLP** — Keyword extraction, regex parsing, and text structuring from unstructured documents
5. **Role-Based Access Control** — Implementing RBAC in Django without third-party libraries
6. **Text-to-Speech** — Offline TTS with pyttsx3 and MP3 file serving over HTTP
7. **Custom User Model** — Extending Django's `AbstractUser` with role-specific profiles
8. **Database Design** — Relational DB design with JSON fields for flexible AI data storage
9. **API Integration** — Consuming Google's `google-genai` SDK with error handling
10. **Full-Stack Development** — End-to-end web app from models to templates

---

## 41. Deployment Readiness

### Current State
The project is **development-ready** (SQLite, `DEBUG=True`). For production deployment, the following changes are needed:

### Pre-Deployment Checklist

```bash
# 1. Set DEBUG=False in .env
DEBUG=False

# 2. Set allowed hosts
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# 3. Configure PostgreSQL (recommended)
pip install psycopg2-binary
DATABASE_URL=postgres://user:password@host:5432/resume_ai

# 4. Collect static files
python manage.py collectstatic

# 5. Use a production SECRET_KEY (generate new one)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 6. Add HTTPS / SSL (via Nginx + Let's Encrypt)

# 7. Use Gunicorn as WSGI server
pip install gunicorn
gunicorn resume_screener.wsgi:application --workers 4

# 8. Use Whitenoise for static files
pip install whitenoise
```

### Recommended Deployment Stack

| Component | Technology |
|-----------|-----------|
| **Web Server** | Nginx |
| **App Server** | Gunicorn |
| **Database** | PostgreSQL |
| **Static Files** | Whitenoise / AWS S3 |
| **Platform** | Railway / Render / AWS EC2 |
| **SSL** | Let's Encrypt (Certbot) |

---

## 42. Testing Strategy

### Unit Tests (Planned)

| Module | Test Cases |
|--------|-----------|
| `accounts` | Registration validation, login, role assignment |
| `resumes` | File upload, parsing, score calculation |
| `jobs` | Job creation, skill parsing, apply logic |
| `applications` | Duplicate check, status updates |
| `ai_services` | Fallback when API key missing, JSON parsing |

### Manual Testing Checklist

- [ ] Register as Candidate → upload resume → view AI score
- [ ] Register as Recruiter → post job → view candidate rankings
- [ ] Apply to job as Candidate → check instant match score
- [ ] Recruiter updates application status → candidate sees update
- [ ] Voice feedback endpoint returns valid audio URL
- [ ] Upload invalid file type → correct error shown
- [ ] Upload file > 10MB → correct error shown
- [ ] Access recruiter-only URL as candidate → redirect to dashboard
- [ ] Admin panel accessible with superuser credentials

### Run Tests

```bash
python manage.py test accounts resumes jobs applications ai_services
```

---

## 43. Performance Optimizations

| Optimization | Implementation |
|-------------|---------------|
| **DB query reduction** | Store `match_score` on `Application` model to avoid re-calling Gemini on page load |
| **Text truncation** | Resume text limited to 5,000 characters before sending to Gemini (reduces API cost + latency) |
| **Lazy AI analysis** | AI suggestions only generated on first resume detail view (not on upload) |
| **DB ordering** | `Application` ordered by `-match_score` at DB level, avoiding Python-side sorting for candidate list |
| **Fallback speed** | Rule-based fallback is instant (no network call), ensuring fast response even during API outages |
| **select_related** | Django ORM `filter()` with `__in` queries used to batch-fetch applications per recruiter |
| **File cleanup** | Physical file deleted from disk on resume delete (prevents storage bloat) |

### Future Performance Improvements (Planned)
- Celery task queue for async AI analysis (non-blocking resume upload)
- Redis caching for frequently accessed job listings
- Pagination for large application/resume lists
- Database indexing on `match_score`, `user_id`, `job_id`

---

## 44. License

```
MIT License

Copyright (c) 2025 Resume AI Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 45. Author Information

| Field | Detail |
|-------|--------|
| **Project** | Resume AI — Intelligent Resume Screening Platform |
| **Framework** | Django 4.x (Python) |
| **AI Engine** | Google Gemini 2.5 Flash |
| **Type** | Full-Stack Web Application |
| **Domain** | HR Technology / AI Recruitment |
| **Status** | Active Development |

### Contact

- **GitHub:** [github.com/your-username](https://github.com/your-username)
- **Email:** your.email@example.com
- **LinkedIn:** [linkedin.com/in/your-profile](https://linkedin.com/in/your-profile)

> ⚠️ **Note:** Update the contact details and GitHub links above with your actual information.

---

<div align="center">

**Built with ❤️ using Django + Google Gemini AI**

*Automating recruitment, one resume at a time.*

[![Made with Django](https://img.shields.io/badge/Made%20with-Django-green?logo=django)](https://djangoproject.com)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Gemini%20AI-orange?logo=google)](https://ai.google.dev)

</div>
