# Quick Start Guide

## For the Impatient ⚡

### Option 1: Docker Compose (Recommended)

```bash
# Clone and navigate
git clone <repository-url>
cd final\ project

# Start all services
docker-compose up -d

# Wait for services to start
sleep 5

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev

# Access frontend at http://localhost:3000
```

## First Steps

1. **Register** at http://localhost:3000/register
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `SecurePass123`

2. **Login** at http://localhost:3000/login
   - Use the credentials above

3. **Update Profile** at http://localhost:3000/profile
   - Change username or email
   - Change password and re-login

4. **View API Docs** at http://localhost:8000/docs
   - Interactive API documentation

## Run Tests

```bash
# Terminal in project root
cd tests
pytest -v

# Or specific tests
pytest test_unit.py -v
pytest test_integration.py -v
```

## Database

```bash
# If using local PostgreSQL
createdb calculator_db -U user
cd backend && alembic upgrade head

# If using Docker
# Database starts automatically with docker-compose up
# Access: psql postgresql://user:password@localhost:5432/calculator_db
```

## Useful Commands

```bash
# View application logs
docker-compose logs -f

# Rebuild images
docker-compose build --no-cache

# Stop services
docker-compose down

# Clean everything
docker-compose down -v

# Make file (if available)
make help           # See all commands
make run-all        # Run backend and frontend
make test           # Run all tests
make docker-up      # Start Docker services
```

## Environment Variables

Create `.env` files if needed:

**backend/.env:**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/calculator_db
SECRET_KEY=your-secret-key-change-in-production
```

**frontend/.env:**
```env
VITE_API_URL=http://localhost:8000
```

## Common Issues

### Port Already in Use
```bash
# Kill process using port
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
```

### Database Connection Error
```bash
# Check if PostgreSQL is running
docker-compose ps db

# Or start it
docker-compose up -d db
```

### Frontend Won't Load API
```bash
# Check backend is running
curl http://localhost:8000/health

# Check CORS headers
curl -i http://localhost:8000/health
```

### Tests Fail
```bash
# Make sure all dependencies are installed
pip install -r backend/requirements.txt

# Reset test database
rm tests/test.db
pytest tests/
```

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- Review [TESTING.md](TESTING.md) for test details
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Architecture Overview

```
┌─────────────────────────────────────┐
│         Frontend (React)             │
│     http://localhost:3000            │
└──────────────┬──────────────────────┘
               │
               │ HTTP/REST API
               │
┌──────────────▼──────────────────────┐
│      Backend (FastAPI)              │
│     http://localhost:8000            │
└──────────────┬──────────────────────┘
               │
               │ SQL
               │
┌──────────────▼──────────────────────┐
│  PostgreSQL Database                │
│ (localhost:5432 or Docker)           │
└─────────────────────────────────────┘
```

## Features

✅ User Registration & Login
✅ JWT Authentication
✅ Profile Management
✅ Password Change
✅ Secure Password Hashing
✅ Responsive UI
✅ Full Test Coverage
✅ Docker Support
✅ CI/CD Pipeline
✅ API Documentation

## Support

- 📖 Documentation: See README.md
- 🐛 Issues: Check GitHub Issues
- 💬 Discussions: Use GitHub Discussions
- 📧 Email: Contact team

Happy coding! 🚀
