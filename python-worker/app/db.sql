CREATE TABLE IF NOT EXISTS job_profiles (
  id SERIAL PRIMARY KEY,
  company_id TEXT NOT NULL,
  company_name TEXT NOT NULL,
  job_id TEXT UNIQUE NOT NULL,
  job_title TEXT NOT NULL,
  department TEXT,
  number_of_openings INTEGER,
  work_mode TEXT,
  job_description TEXT,
  posting_date DATE,
  closing_date DATE,
  starting_date DATE,
  duration TEXT,
  locations JSONB,
  requirements JSONB,
  employment_details JSONB,
  required_documents JSONB,
  contact JSONB,
  status TEXT DEFAULT 'PUBLISHED',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS job_applications (
  id SERIAL PRIMARY KEY,
  job_id TEXT NOT NULL REFERENCES job_profiles(job_id) ON DELETE CASCADE,
  full_name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  linkedin_url TEXT,
  cover_letter TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
