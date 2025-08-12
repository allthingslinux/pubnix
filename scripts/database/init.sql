-- ATL Pubnix Database Initialization
-- Development database setup

-- Create database if it doesn't exist (for development)
-- Note: This file is run by PostgreSQL docker-entrypoint-initdb.d

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create basic tables for development
-- These will be properly managed by Alembic migrations in production

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(32) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    application_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    approval_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'pending',
    home_directory VARCHAR(255),
    shell VARCHAR(255) DEFAULT '/bin/bash',
    last_login TIMESTAMP WITH TIME ZONE,
    created_by VARCHAR(32),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS resource_limits (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    disk_quota_mb INTEGER DEFAULT 1024,
    max_processes INTEGER DEFAULT 50,
    cpu_limit_percent INTEGER DEFAULT 10,
    memory_limit_mb INTEGER DEFAULT 512,
    max_login_sessions INTEGER DEFAULT 5,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS applications (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    username_requested VARCHAR(32) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    motivation TEXT,
    community_guidelines_accepted BOOLEAN DEFAULT FALSE,
    application_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'pending',
    reviewed_by VARCHAR(32),
    review_date TIMESTAMP WITH TIME ZONE,
    review_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);
CREATE INDEX IF NOT EXISTS idx_applications_email ON applications(email);

-- Insert development test data
INSERT INTO users (username, email, full_name, status, approval_date, home_directory, created_by) 
VALUES 
    ('testuser1', 'testuser1@example.com', 'Test User One', 'approved', NOW(), '/home/testuser1', 'admin'),
    ('testuser2', 'testuser2@example.com', 'Test User Two', 'approved', NOW(), '/home/testuser2', 'admin')
ON CONFLICT (username) DO NOTHING;

INSERT INTO resource_limits (user_id, disk_quota_mb, max_processes, cpu_limit_percent, memory_limit_mb, max_login_sessions)
SELECT id, 1024, 50, 10, 512, 5 FROM users WHERE username IN ('testuser1', 'testuser2')
ON CONFLICT DO NOTHING;