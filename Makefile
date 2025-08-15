.PHONY: help install dev test clean docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  dev         - Run development servers"
	@echo "  test        - Run tests"
	@echo "  docker-up   - Start with Docker"
	@echo "  docker-down - Stop Docker containers"

install:
	cd API && pip install -r requirements.txt
	cd WEB && pip install -r requirements.txt

dev:
	@echo "Starting API server..."
	cd API && uvicorn run:app --reload --port 8000 &
	@echo "Starting Django server..."
	cd WEB && python manage.py runserver 8080

test:
	cd API && pytest
	cd WEB && python manage.py test

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete