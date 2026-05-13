# Contributing Guidelines

## Welcome!

Thank you for your interest in contributing to the Calculator App! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Report issues responsibly
- Support other contributors

## Getting Started

### Prerequisites

- Git
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker & Docker Compose (optional)

### Setup Development Environment

```bash
# Clone repository
git clone <repository-url>
cd final\ project

# Create feature branch
git checkout -b feature/your-feature-name

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup frontend
cd ../frontend
npm install

# Start development servers
# Terminal 1: Backend
cd backend && uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev

# Terminal 3: Database (if local)
# Ensure PostgreSQL is running
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/user-profile-improvements
# or
git checkout -b bugfix/password-validation
# or
git checkout -b docs/add-api-examples
```

Branch naming convention:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation
- `test/` - Test additions
- `refactor/` - Code improvements

### 2. Make Changes

#### Backend Changes

- Follow PEP 8 style guide
- Add type hints
- Write docstrings
- Update related tests

```python
def change_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Change user password.
    
    Args:
        password_data: New password data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Success message and updated user
        
    Raises:
        HTTPException: If password is incorrect or validation fails
    """
```

#### Frontend Changes

- Follow React best practices
- Use functional components with hooks
- Add proper prop types/validation
- Keep components focused and reusable

```jsx
function Profile({ setIsAuthenticated }) {
  const [user, setUser] = React.useState(null)
  const [loading, setLoading] = React.useState(true)
  
  React.useEffect(() => {
    fetchProfile()
  }, [])
  
  return (...)
}
```

### 3. Test Your Changes

```bash
# Run unit tests
pytest tests/test_unit.py -v

# Run integration tests
pytest tests/test_integration.py -v

# Run E2E tests
pytest tests/test_e2e.py -v

# Run all tests with coverage
pytest --cov=backend --cov-report=html

# Format code
black backend/
# (Frontend formatting is in ESLint config)

# Lint code
flake8 backend/
cd frontend && npm run lint
```

### 4. Commit Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "feature: add password change functionality

- Implement password change endpoint
- Add password validation
- Update user profile page UI
- Add integration tests for password change"
```

Commit message format:
- Type: `feature`, `bugfix`, `docs`, `test`, `refactor`
- Subject: Clear and concise
- Body: Detailed explanation (optional)
- References: Link related issues (fixes #123)

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub:

#### PR Title Format
```
[type] Brief description (fixes #issue-number)

feature: Add password change functionality (fixes #45)
bugfix: Fix email validation in profile update
docs: Add deployment guide
```

#### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Performance improvement
- [ ] Code refactoring

## Related Issues
Fixes #123

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] Code coverage maintained/improved

## Changes
- List major changes
- List files modified

## Screenshots/Demo
(if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No new warnings generated
```

## Code Style Guidelines

### Python (Backend)

```python
# Use type hints
def validate_email(email: str) -> bool:
    """Validate email format."""
    pass

# Use docstrings
def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)

# Follow PEP 8
# - Use 4 spaces for indentation
# - Max line length: 88 characters
# - Use descriptive variable names

# Use logging
import logging
logger = logging.getLogger(__name__)
logger.info("User registered: %s", username)
```

### JavaScript/React (Frontend)

```jsx
// Use functional components with hooks
function MyComponent({ title, onSubmit }) {
  const [state, setState] = React.useState('')
  
  return (
    <div className="container">
      <h1>{title}</h1>
    </div>
  )
}

// Use meaningful names
const isValidEmail = (email) => email.includes('@')

// Use prop validation
MyComponent.propTypes = {
  title: PropTypes.string.isRequired,
  onSubmit: PropTypes.func.isRequired,
}

// Export at bottom
export default MyComponent
```

### CSS

```css
/* Use BEM naming */
.profile-section {
  margin-bottom: 20px;
}

.profile-section__header {
  font-weight: bold;
}

.profile-section--highlighted {
  background-color: yellow;
}

/* Use variables */
:root {
  --primary-color: #667eea;
  --spacing-unit: 8px;
}

.button {
  color: var(--primary-color);
  padding: var(--spacing-unit);
}
```

## Testing Guidelines

### Write Tests For

- All new functions/endpoints
- Bug fixes (add regression test)
- Edge cases
- Error scenarios

### Test Structure

```python
class TestFeatureName:
    """Test feature description."""
    
    def test_success_case(self):
        """Test successful scenario."""
        # Arrange
        test_data = {...}
        
        # Act
        result = function(test_data)
        
        # Assert
        assert result == expected
    
    def test_error_case(self):
        """Test error scenario."""
        with pytest.raises(ValueError):
            function(invalid_data)
```

### Test Coverage Requirements

- New code: Minimum 80% coverage
- Modified code: Maintain or improve coverage
- Use `pytest --cov` to check coverage

## Documentation

### Update Documentation For

- New features
- API changes
- Configuration changes
- Bug fixes (if behavioral)

### Documentation Format

- Use Markdown
- Include code examples
- Add diagrams where helpful
- Keep README up to date

### Example Documentation

```markdown
## Feature: Password Change

### Description
Users can now change their password from the profile page.

### API Endpoint
POST /api/profile/change-password

### Request
\`\`\`json
{
  "old_password": "string",
  "new_password": "string",
  "confirm_password": "string"
}
\`\`\`

### Usage
1. Navigate to Profile
2. Click "Change Password"
3. Enter old password
4. Enter new password (minimum 8 characters)
5. Confirm new password
6. Click "Update Password"
```

## Pull Request Review Process

### For Contributors

- Make sure CI/CD passes
- Respond to review feedback
- Keep commits organized
- Update PR description if changes are made

### For Reviewers

- Review code for correctness
- Check test coverage
- Suggest improvements
- Be respectful and constructive

### Merge Criteria

- [ ] All CI/CD checks pass
- [ ] At least 2 approvals
- [ ] No conflicts with main branch
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated

## Reporting Issues

### Bug Report

```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. Go to...
2. Click...
3. See error...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g. macOS]
- Browser: [e.g. Chrome]
- Python Version: [e.g. 3.11]
- Node Version: [e.g. 18]

## Logs/Screenshots
Attach relevant error messages or screenshots
```

### Feature Request

```markdown
## Summary
Brief description of feature

## Motivation
Why this feature is needed

## Proposed Solution
How it should work

## Alternative Solutions
Other possible approaches

## Additional Context
Any other relevant information
```

## Performance Optimization

### Backend
- Use async/await for I/O operations
- Implement database query optimization
- Add caching for frequently accessed data
- Use connection pooling

### Frontend
- Code splitting with React.lazy
- Image optimization
- CSS/JS minification
- Lazy load components

## Security

### Report Security Issues

**DO NOT** open public issues for security vulnerabilities.

Instead:
1. Email security@yourdomain.com
2. Include detailed description
3. Wait for acknowledgment
4. Do not disclose publicly until patch is released

### Security Best Practices

- Never commit secrets
- Use environment variables
- Validate all inputs
- Sanitize output
- Use HTTPS in production
- Keep dependencies updated

## Resources

- [Git Workflow](https://www.atlassian.com/git)
- [PEP 8 Style Guide](https://pep8.org/)
- [React Best Practices](https://react.dev/)
- [Commit Message Guidelines](https://conventionalcommits.org/)

## Questions?

- Check existing issues
- Review documentation
- Ask in discussions
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Recognition

Contributors will be recognized in:
- Project README
- Release notes
- Contributors page

Thank you for contributing! 🎉
