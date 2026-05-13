# Calculator App with User Profile Management

A full-stack application featuring a FastAPI backend with user authentication and profile management, and a React frontend with a modern UI.

## Features

- **User Authentication**: Secure registration and login with JWT tokens
- **User Profile Management**: Update username and email
- **Password Management**: Secure password change with hashing (bcrypt)
- **Responsive UI**: Built with React and CSS
- **Comprehensive Testing**: Unit, integration, and E2E tests
- **Docker Deployment**: Containerized backend and frontend
- **CI/CD Pipeline**: Automated testing and Docker Hub deployment

## Project Structure

```
.
├── backend/                    # FastAPI backend
│   ├── main.py                # Main application
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── security.py            # Authentication & password hashing
│   ├── database.py            # Database configuration
│   ├── config.py              # Application settings
│   ├── requirements.txt        # Python dependencies
│   ├── alembic/               # Database migrations
│   └── .env.example           # Example environment variables
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── pages/             # Page components (Login, Register, Profile, Dashboard)
│   │   ├── components/        # Reusable components
│   │   ├── styles/            # CSS stylesheets
│   │   └── main.jsx           # Entry point
│   ├── package.json           # Node dependencies
│   ├── vite.config.js         # Vite configuration
│   └── .env.example           # Example environment variables
├── tests/                     # Test suite
│   ├── test_unit.py           # Unit tests
│   ├── test_integration.py    # Integration tests
│   └── test_e2e.py            # End-to-end tests (Playwright)
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile.backend         # Backend Docker image
├── Dockerfile.frontend        # Frontend Docker image
└── .github/workflows/         # CI/CD pipelines
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker & Docker Compose (for containerized deployment)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd final\ project
```

### 2. Backend Setup

#### Option A: Local Development

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database URL and settings

# Run database migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

#### Option B: Docker

```bash
# From project root
docker-compose up -d db backend
```

### 3. Frontend Setup

#### Option A: Local Development

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Edit .env with your API URL

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

#### Option B: Docker

```bash
# From project root
docker-compose up -d frontend
```

### 4. Full Stack with Docker Compose

```bash
# From project root, start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Database Setup

### Using PostgreSQL Locally

```bash
# Create database
createdb calculator_db -U user

# Set password for user
psql -U postgres -d calculator_db -c "ALTER USER user WITH PASSWORD 'password';"

# Run migrations
cd backend
alembic upgrade head
```

### Using PostgreSQL with Docker

The Docker Compose file automatically sets up PostgreSQL with:
- Username: `user`
- Password: `password`
- Database: `calculator_db`

## Running Tests

### Unit Tests

```bash
cd tests
pytest test_unit.py -v
```

Tests for:
- Password hashing and verification
- JWT token creation and verification
- Token expiration and tampering detection

### Integration Tests

```bash
cd tests
pytest test_integration.py -v
```

Tests for:
- User registration and login
- Profile updates (username, email)
- Password change flow
- Authorization and authentication
- Error handling

### E2E Tests

```bash
cd tests
pytest test_e2e.py -v

# Or run with Playwright
npx playwright test
```

Tests for:
- Complete registration flow
- Login and dashboard access
- Profile update workflow
- Password change and re-login
- Error handling and validation

### Run All Tests with Coverage

```bash
cd tests
pytest --cov=backend --cov-report=html
```

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
  ```json
  {
    "username": "string",
    "email": "user@example.com",
    "password": "string"
  }
  ```

- `POST /api/auth/login` - Login user
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

### Profile

- `GET /api/profile` - Get current user profile (requires auth)
- `PUT /api/profile` - Update user profile (requires auth)
  ```json
  {
    "username": "string (optional)",
    "email": "user@example.com (optional)"
  }
  ```

- `POST /api/profile/change-password` - Change password (requires auth)
  ```json
  {
    "old_password": "string",
    "new_password": "string",
    "confirm_password": "string"
  }
  ```

### Health

- `GET /health` - Health check

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/calculator_db
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

## Deployment to Docker Hub

### Prerequisites

- Docker Hub account
- Docker installed locally

### Steps

1. **Build images locally**
   ```bash
   docker build -f Dockerfile.backend -t yourusername/calculator-backend:latest .
   docker build -f Dockerfile.frontend -t yourusername/calculator-frontend:latest .
   ```

2. **Login to Docker Hub**
   ```bash
   docker login
   ```

3. **Push images**
   ```bash
   docker push yourusername/calculator-backend:latest
   docker push yourusername/calculator-frontend:latest
   ```

4. **Pull and run on production**
   ```bash
   docker pull yourusername/calculator-backend:latest
   docker pull yourusername/calculator-frontend:latest
   docker-compose up -d
   ```

### GitHub Actions CI/CD

The repository includes an automated CI/CD pipeline (`.github/workflows/ci-cd.yml`) that:

1. Runs all tests on every push to `main` or `develop`
2. Builds Docker images on successful tests
3. Pushes images to Docker Hub on merge to `main`

**To enable GitHub Actions:**

1. Go to your GitHub repository settings
2. Add secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password token
3. Commit and push to trigger the workflow

## Development Workflow

### Making Changes

1. Create a feature branch
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make your changes and test locally

3. Run tests
   ```bash
   cd tests
   pytest -v
   ```

4. Commit and push
   ```bash
   git add .
   git commit -m "Add my feature"
   git push origin feature/my-feature
   ```

5. Create a Pull Request

### Testing Changes

After making backend changes:
```bash
cd tests
pytest test_unit.py test_integration.py -v
```

After making frontend changes:
```bash
cd frontend
npm run build
npm run preview
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
psql -U user -d calculator_db -c "SELECT 1;"

# Or with Docker
docker-compose logs db
```

### Backend not starting

```bash
# Check logs
docker-compose logs backend

# Verify database is ready
docker-compose logs db

# Ensure migrations are applied
docker-compose exec backend alembic upgrade head
```

### Frontend not loading

```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Tests failing

```bash
# Reset test database
cd tests
pytest --tb=short -v

# Check test logs
pytest test_integration.py -v -s
```

## Security Considerations

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- CORS middleware for cross-origin requests
- Environment variables for sensitive data
- Input validation with Pydantic schemas
- SQL injection prevention with SQLAlchemy ORM

## Performance Optimization

- Database connection pooling
- Indexed columns for faster queries
- Async request handling with FastAPI
- Frontend code splitting with Vite
- CSS modules for style scoping

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please:
- Create an issue on GitHub
- Submit a pull request
- Contact the development team

## Docker Hub Repository

**Backend**: `https://hub.docker.com/r/yourusername/calculator-backend`

**Frontend**: `https://hub.docker.com/r/yourusername/calculator-frontend`

Replace `yourusername` with your actual Docker Hub username.

## Changelog

### Version 1.0.0
- Initial release with user authentication
- User profile management
- Password change functionality
- Complete test coverage
- Docker deployment
- CI/CD pipeline
