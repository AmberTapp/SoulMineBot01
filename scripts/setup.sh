#!/bin/bash

# Initial setup script for SoulMine Telegram Bot

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please update .env file with your values"
fi

# Create necessary directories
mkdir -p logs media static backups certbot/conf certbot/www nginx/conf.d

# Set permissions
chmod +x scripts/*.sh

# Build containers
echo "Building containers..."
docker-compose build

# Initialize database
echo "Initializing database..."
docker-compose up -d postgres redis
sleep 10

# Run database initialization
docker-compose exec postgres psql -U soulmine -d soulmine_db -f /docker-entrypoint-initdb.d/init.sql

echo "Setup completed!"
echo "Run 'docker-compose up -d' to start all services"