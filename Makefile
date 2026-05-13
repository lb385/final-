.PHONY: help setup install-backend install-frontend run-backend run-frontend run-all test test-unit test-integration test-e2e clean docker-up docker-down docker-build lint format migrate

help:
	@echo "Calculator App - Available Commands"
	@echo "===================================="
	@echo "Setup:"
	@echo "  make setup              - Complete setup (install dependencies)"
	@echo "  make install-backend    - Install backend dependencies"
	@echo "  make install-frontend   - Install frontend dependencies"
	@echo ""
	@echo "Running:"
	@echo "  make run-backend        - Run backend server (requires PostgreSQL)"
	@echo "  make run-frontend       - Run frontend dev server"
	@echo "  make run-all            - Run all services locally"
	@echo ""
	@echo "Testing:"
	@echo "  make test               - Run all tests"
	@echo "  make test-unit          - Run unit tests"
	@echo "  make test-integration   - Run integration tests"
	@echo "  make test-e2e           - Run E2E tests"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build       - Build Docker images"
	@echo "  make docker-up          - Start Docker services"
	@echo "  make docker-down        - Stop Docker services"
	@echo ""
	@echo "Maintenance:"
	@echo "  make migrate            - Run database migrations"
	@echo "  make lint               - Run linter"
	@echo "  make format             - Format code"
	@echo "  make clean              - Clean up generated files"

setup: install-backend install-frontend

install-backend:
	cd backend && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

run-backend:
	cd backend && uvicorn main:app --reload

run-frontend:
	cd frontend && npm run dev

run-all:
	@echo "Starting backend and frontend..."
	@echo "Backend running at http://localhost:8000"
	@echo "Frontend running at http://localhost:3000"
	cd backend && uvicorn main:app --reload & \
	cd frontend && npm run dev

test:
	cd tests && pytest -v --tb=short

test-unit:
	cd tests && pytest test_unit.py -v --tb=short

test-integration:
	cd tests && pytest test_integration.py -v --tb=short

test-e2e:
	cd tests && pytest test_e2e.py -v --tb=short

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf build dist *.egg-info
	rm -rf backend/test.db tests/test.db
	cd frontend && rm -rf dist node_modules

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

migrate:
	cd backend && alembic upgrade head

lint:
	cd backend && flake8 .
	cd frontend && npm run lint

format:
	cd backend && black .
	cd frontend && npm run format || true

.PHONY: help setup install-backend install-frontend run-backend run-frontend run-all test test-unit test-integration test-e2e docker-build docker-up docker-down clean
