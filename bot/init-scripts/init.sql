-- Create database extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    telegram_id VARCHAR(36) UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    language_code VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW() ON UPDATE NOW(),
    last_interaction TIMESTAMP,
    wallet_address VARCHAR(255),
    verified BOOLEAN DEFAULT FALSE,
    subscription_status VARCHAR(20) DEFAULT 'free',
    subscription_end_date TIMESTAMP,
    referral_code VARCHAR(50) UNIQUE,
    referred_by VARCHAR(36) REFERENCES users(id),
    total_points INTEGER DEFAULT 0,
    loyalty_level INTEGER DEFAULT 1,
    notifications_enabled BOOLEAN DEFAULT TRUE,
    preferences JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}'
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_wallet_address ON users(wallet_address);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
CREATE INDEX IF NOT EXISTS idx_users_last_interaction ON users(last_interaction);
CREATE INDEX IF NOT EXISTS idx_users_referral_code ON users(referral_code);

-- Create initial admin user
INSERT INTO users (id, telegram_id, username, first_name, last_name, language_code, is_active, created_at, updated_at, last_interaction, wallet_address, verified, subscription_status, subscription_end_date, referral_code, referred_by, total_points, loyalty_level, notifications_enabled, preferences, metadata)
VALUES ('admin-1', '123456789', 'admin_user', 'Admin', 'User', 'en', TRUE, NOW(), NOW(), NOW(), 'UQCvDWfIeYiSCeCyREOBxJuLpLWBoeBCip7aGEMVX-9xwRBy', TRUE, 'premium', NOW() + INTERVAL '1 year', 'REF-ADMIN-1234', NULL, 10000, 5, TRUE, '{"theme": "dark"}', '{"admin": true}')
ON CONFLICT (telegram_id) DO NOTHING;

-- Create sample users for testing
INSERT INTO users (id, telegram_id, username, first_name, last_name, language_code, is_active, created_at, updated_at, last_interaction, wallet_address, verified, subscription_status, subscription_end_date, referral_code, referred_by, total_points, loyalty_level, notifications_enabled, preferences, metadata)
VALUES 
('user-1', '987654321', 'john_doe', 'John', 'Doe', 'en', TRUE, NOW(), NOW(), NOW(), 'UQABCD1234567890', TRUE, 'premium', NOW() + INTERVAL '6 months', 'REF-JOHN-5678', 'admin-1', 5000, 4, TRUE, '{"theme": "light"}', '{}'),
('user-2', '567890123', 'jane_smith', 'Jane', 'Smith', 'ru', TRUE, NOW(), NOW(), NOW(), 'UQEF1234567890', TRUE, 'free', NULL, 'REF-JANE-1234', 'admin-1', 2000, 3, TRUE, '{"theme": "dark"}', '{}')
ON CONFLICT (telegram_id) DO NOTHING;

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_users_subscription_status ON users(subscription_status);
CREATE INDEX IF NOT EXISTS idx_users_loyalty_level ON users(loyalty_level);
CREATE INDEX IF NOT EXISTS idx_users_notifications_enabled ON users(notifications_enabled);