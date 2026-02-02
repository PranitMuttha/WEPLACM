import os
import json
from typing import Any, Dict, List, Optional

import psycopg2
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


# -----------------------
# CONFIG (edit or set env vars)
# -----------------------
DB_HOST = os.getenv("DB_HOST", "141.26.156.184")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "my_database")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "password")

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8080"))  # you asked 8080


def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )


def safe_json(obj: Any, fallback):
    if obj is None:
        return fallback
    if isinstance(obj, (dict, list)):
        return obj
    # if it's already a JSON string:
    try:
        return json.loads(obj)
    except Exception:
        return fallback


app = FastAPI(title="WEPLACM Job Site")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# -----------------------
# UI PAGES
# -----------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/jobs", response_class=HTMLResponse)
def jobs_list(request: Request):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT job_id, job_title, company_name, work_mode, department, created_at
        FROM job_profiles
        WHERE status IN ('PUBLISHED','RECEIVED')
        ORDER BY created_at DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    jobs = [
        {
            "job_id": r[0],
            "job_title": r[1],
            "company_name": r[2],
            "work_mode": r[3],
            "department": r[4],
            "created_at": r[5],
        }
        for r in rows
    ]

    return templates.TemplateResponse("jobs.html", {"request": request, "jobs": jobs})


@app.get("/jobs/{job_id}", response_class=HTMLResponse)
def job_detail(request: Request, job_id: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT job_id, job_title, company_name, company_id, department,
               number_of_openings, work_mode, job_description,
               locations, requirements, employment_details, required_documents, contact,
               posting_date, closing_date, starting_date, duration, status, created_at
        FROM job_profiles
        WHERE job_id = %s
    """, (job_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Job not found")

    cur.execute("SELECT COUNT(*) FROM job_profiles  WHERE job_id=%s", (job_id,))
    application_count = cur.fetchone()[0]

    cur.close()
    conn.close()

    job = {
        "job_id": row[0],
        "job_title": row[1],
        "company_name": row[2],
        "company_id": row[3],
        "department": row[4],
        "number_of_openings": row[5],
        "work_mode": row[6],
        "job_description": row[7] or "",
        "locations": safe_json(row[8], []),
        "requirements": safe_json(row[9], {}),
        "employment_details": safe_json(row[10], {}),
        "required_documents": safe_json(row[11], []),
        "contact": safe_json(row[12], {}),
        "posting_date": row[13],
        "closing_date": row[14],
        "starting_date": row[15],
        "duration": row[16],
        "status": row[17],
        "created_at": row[18],
        "application_count": application_count,
    }

    return templates.TemplateResponse("job_detail.html", {"request": request, "job": job})


@app.get("/jobs/{job_id}/apply", response_class=HTMLResponse)
def apply_page(request: Request, job_id: str):
    # Confirm job exists
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT job_id, job_title, company_name FROM job_profiles WHERE job_id=%s", (job_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Job not found")

    job = {"job_id": row[0], "job_title": row[1], "company_name": row[2]}
    return templates.TemplateResponse("apply.html", {"request": request, "job": job})


@app.post("/jobs/{job_id}/apply")
def apply_submit(
    request: Request,
    job_id: str,
    full_name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    linkedin_url: Optional[str] = Form(None),
    cover_letter: Optional[str] = Form(None),
):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM job_profiles WHERE job_id=%s", (job_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Job not found")

    cur.execute("""
        INSERT INTO job_applications(job_id, full_name, email, phone, linkedin_url, cover_letter)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (job_id, full_name, email, phone, linkedin_url, cover_letter))

    conn.commit()
    cur.close()
    conn.close()

    return RedirectResponse(url=f"/jobs/{job_id}/apply/success", status_code=303)


@app.get("/jobs/{job_id}/apply/success", response_class=HTMLResponse)
def apply_success(request: Request, job_id: str):
    return templates.TemplateResponse("apply_success.html", {"request": request, "job_id": job_id})


# -----------------------
# OPTIONAL: API endpoints (useful for Camunda worker debugging)
# -----------------------
@app.get("/api/jobs")
def api_jobs():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT job_id, job_title, company_name, work_mode, department, created_at
        FROM job_profiles
        WHERE status IN ('PUBLISHED','RECEIVED')
        ORDER BY created_at DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "job_id": r[0],
            "job_title": r[1],
            "company_name": r[2],
            "work_mode": r[3],
            "department": r[4],
            "created_at": str(r[5]),
        }
        for r in rows
    ]
