-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create schema for Concilium IQ
CREATE SCHEMA IF NOT EXISTS concilium;

-- Note: Tables are created by SQLAlchemy/Alembic migrations
-- This script only enables extensions needed by the application
