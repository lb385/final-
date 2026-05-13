# Testing Guide

## Overview

This project includes comprehensive testing coverage with unit tests, integration tests, and end-to-end (E2E) tests.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py          # Pytest configuration and fixtures
├── test_unit.py         # Unit tests (~40 tests)
├── test_integration.py  # Integration tests (~50 tests)
├── test_e2e.py         # End-to-end tests with Playwright (~30 tests)
└── pytest.ini          # Pytest configuration
```

## Running Tests

### Prerequisites

```bash
# Install backend dependencies
pip install -r backend/requirements.txt

# Install test dependencies
pip install pytest pytest-asyncio httpx

# For E2E tests
pip install playwright
playwright install chromium
```

### Run All Tests

```bash
cd tests
pytest -v
```

### Run Specific Test Types

```bash
# Unit tests only
pytest test_unit.py -v

# Integration tests only
pytest test_integration.py -v

# E2E tests only
pytest test_e2e.py -v

# Specific test class
pytest test_unit.py::TestPasswordHashing -v

# Specific test function
pytest test_unit.py::TestPasswordHashing::test_hash_password_creates_hash -v
```

### Run Tests with Coverage

```bash
# Generate coverage report
pytest --cov=backend --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html
```

### Run Tests in Parallel

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run with 4 workers
pytest -n 4
```

## Unit Tests

Located in `test_unit.py`

### What They Test

- **Password Hashing**
  - Hash generation
  - Password verification
  - Incorrect password detection
  - Different hash generation

- **Token Management**
  - JWT token creation
  - Token verification
  - Invalid token detection
  - Tampered token detection

### Running Unit Tests

```bash
pytest test_unit.py -v

# Or with coverage
pytest test_unit.py -v --cov=backend.security
```

### Example Unit Test

```python
def test_hash_password_correct(self):
    """Test that verify_password works with correct password."""
    password = "testpassword123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True
```

## Integration Tests

Located in `test_integration.py`

### What They Test

- **Authentication Routes**
  - User registration
  - Duplicate username/email handling
  - User login
  - Invalid credentials

- **Profile Routes**
  - Get user profile
  - Update username
  - Update email
  - Change password (valid)
  - Change password (invalid old password)
  - Change password (mismatched new passwords)
  - Authorization checks

- **Health Checks**
  - Server health endpoint

### Running Integration Tests

```bash
# Start PostgreSQL first (or use Docker)
docker-compose up -d db

# Run integration tests
cd tests
pytest test_integration.py -v

# Or with coverage
pytest test_integration.py -v --cov=backend
```

### Example Integration Test

```python
def test_register_user_success(self):
    """Test successful user registration."""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
```

## End-to-End (E2E) Tests

Located in `test_e2e.py`

### What They Test

- **Complete Registration Flow**
  - Register new user
  - Verify account creation
  - Login after registration

- **Profile Update Workflow**
  - Login
  - Navigate to profile
  - Update profile information
  - Verify changes persist

- **Password Change Workflow**
  - Login
  - Navigate to profile
  - Change password
  - Logout
  - Login with new password

- **Error Handling**
  - Invalid password change
  - Duplicate username detection
  - Missing fields validation

### Prerequisites for E2E Tests

```bash
# Install Playwright
pip install playwright
playwright install chromium

# Or install all browsers
playwright install
```

### Running E2E Tests

```bash
# Start services first
docker-compose up -d

# Wait for services to be ready (10 seconds)
sleep 10

# Run E2E tests
cd tests
pytest test_e2e.py -v

# Or with Playwright directly
npx playwright test
```

### Debugging E2E Tests

```bash
# Run with headed mode (see browser)
pytest test_e2e.py -v -s --headed

# Run with tracing
pytest test_e2e.py -v --trace on

# View trace
playwright show-trace trace.zip
```

### Example E2E Test

```python
def test_change_password_flow(self, page: Page):
    """Test password change workflow."""
    # Register
    page.goto(f"{BASE_URL}/register")
    page.fill('input[name="username"]', "pwduser")
    page.fill('input[name="password"]', "InitialPass123")
    page.click('button[type="submit"]')
    
    # Login
    page.wait_for_url("**/login")
    page.fill('input[name="username"]', "pwduser")
    page.fill('input[name="password"]', "InitialPass123")
    page.click('button[type="submit"]')
    
    # Change password
    page.click('a[href="/profile"]')
    page.click('button:has-text("Change Password")')
    page.fill('input[name="oldPassword"]', "InitialPass123")
    page.fill('input[name="newPassword"]', "NewPass456")
    page.click('button:has-text("Update Password")')
    
    # Verify
    page.wait_for_selector('text=Password changed successfully')
```

## Test Configuration

### pytest.ini

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --strict-markers --tb=short
asyncio_mode = auto

markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
```

### conftest.py

Contains pytest fixtures and configuration:
- Event loop for async tests
- Database setup and teardown
- Test client creation

## Continuous Integration

### GitHub Actions

Configured in `.github/workflows/ci-cd.yml`

**On every push to main/develop:**

1. ✅ Run unit tests
2. ✅ Run integration tests
3. ✅ Run coverage analysis
4. ✅ Build Docker images
5. ✅ Push to Docker Hub (on main branch)

**To enable CI/CD:**

1. Add GitHub secrets:
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`

2. GitHub Actions automatically runs on:
   - Push to `main` or `develop`
   - Pull requests to `main` or `develop`

### View CI/CD Status

- GitHub Actions tab in repository
- Check specific workflow run
- View logs for failed tests

## Test Data and Fixtures

### Using Fixtures

```python
@pytest.fixture
def auth_header(self):
    """Create test user and return auth header."""
    # Setup
    client.post("/api/auth/register", json={...})
    response = client.post("/api/auth/login", json={...})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
    # Teardown automatic
```

### Database Cleanup

Integration tests automatically:
- Create test database
- Drop/recreate tables before each test
- Clean up after all tests

## Performance Testing

```bash
# Install locust
pip install locust

# Create load test
# locustfile.py
from locust import HttpUser, task

class ApiUser(HttpUser):
    @task
    def health_check(self):
        self.client.get("/health")

# Run load test
locust -f locustfile.py --host=http://localhost:8000
```

## Accessibility Testing

For frontend E2E tests, verify accessibility:

```javascript
// Use axe-playwright for accessibility
import { injectAxe, checkA11y } from 'axe-playwright'

test('page should be accessible', async ({ page }) => {
  await page.goto('/login')
  await injectAxe(page)
  await checkA11y(page)
})
```

## Security Testing

### OWASP Testing

```bash
# Install OWASP ZAP
brew install zaproxy

# Scan application
zaproxy -cmd -quickurl http://localhost:3000 -quickout report.html
```

### Dependency Scanning

```bash
# Check for vulnerable dependencies
pip install safety
safety check

# Or with npm
npm audit
```

## Test Reporting

### Generate HTML Report

```bash
pytest --html=report.html --self-contained-html
open report.html
```

### Generate JUnit XML

```bash
pytest --junit-xml=results.xml
```

### Coverage Reports

```bash
# Terminal report
pytest --cov=backend --cov-report=term-missing

# HTML report
pytest --cov=backend --cov-report=html
open htmlcov/index.html

# Coverage badge
pip install coverage-badge
coverage-badge -o coverage.svg -f
```

## Troubleshooting Tests

### Common Issues

**Import Errors**
```bash
# Make sure path is set correctly
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"
pytest tests/test_integration.py -v
```

**Database Connection Errors**
```bash
# Ensure PostgreSQL is running
docker-compose up -d db

# Or use SQLite for local testing
# Update SQLALCHEMY_DATABASE_URL in test_integration.py
```

**Playwright Timeout**
```bash
# Increase timeout in test
page.wait_for_selector('text=...', timeout=10000)

# Or set globally
pytest.fixture(scope="session")
def browser():
    return sync_playwright().start().chromium.launch()
```

**Flaky E2E Tests**
```bash
# Add waits
page.wait_for_load_state("networkidle")

# Use explicit waits
page.wait_for_selector("button")
page.wait_for_url("**/dashboard")

# Or run with retries
pytest test_e2e.py -v --maxfail=2
```

## Best Practices

1. **Keep tests isolated** - No dependencies between tests
2. **Use descriptive names** - Clearly state what is being tested
3. **Test one thing** - Each test should test one behavior
4. **Use fixtures** - Share common setup code
5. **Mock external services** - Isolate units being tested
6. **Cleanup after tests** - Ensure no side effects
7. **Document tests** - Explain the test purpose
8. **Run locally first** - Before committing
9. **Monitor coverage** - Aim for >80% coverage
10. **Review test logs** - Understand failures

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Playwright Documentation](https://playwright.dev/)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/faq/testing.html)

## Support

For testing issues:
- Review test output logs
- Check test configuration
- Ensure all dependencies are installed
- Review test-specific documentation
