#!/bin/bash

# Production deployment script for SoulMine Telegram Bot

# Check if running on production server
if [ "$DEPLOY_ENV" != "production" ]; then
  echo "This script should only be run in production environment"
  exit 1
fi

# Pull latest code
git pull origin main

# Build Docker images
docker-compose build

# Stop current services
docker-compose down

# Start new services
docker-compose up -d

# Run database migrations (if any)
# docker-compose exec bot python -c "from bot.utils.database import init_db; init_db()"

# Restart services to apply changes
docker-compose restart

# Clean up old images
docker image prune -f

echo "Production deployment completed successfully!"