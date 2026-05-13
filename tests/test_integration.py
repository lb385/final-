import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import Base, get_db
from main import app
from models import User
from security import hash_password
from schemas import UserCreate, LoginRequest

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_db():
    """Clean up database before and after each test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

class TestAuthenticationRoutes:
    """Test authentication endpoints."""
    
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
        assert data["email"] == "test@example.com"
        assert "id" in data
    
    def test_register_duplicate_username(self):
        """Test registration fails with duplicate username."""
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpass123"
            }
        )
        response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "another@example.com",
                "password": "testpass123"
            }
        )
        assert response.status_code == 400
    
    def test_login_success(self):
        """Test successful login."""
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpass123"
            }
        )
        response = client.post(
            "/api/auth/login",
            json={
                "username": "testuser",
                "password": "testpass123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["username"] == "testuser"
    
    def test_login_invalid_credentials(self):
        """Test login fails with invalid credentials."""
        response = client.post(
            "/api/auth/login",
            json={
                "username": "nonexistent",
                "password": "wrongpass"
            }
        )
        assert response.status_code == 401

class TestProfileRoutes:
    """Test profile management endpoints."""
    
    @pytest.fixture
    def auth_header(self):
        """Create a test user and return auth header."""
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpass123"
            }
        )
        response = client.post(
            "/api/auth/login",
            json={
                "username": "testuser",
                "password": "testpass123"
            }
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_get_profile(self, auth_header):
        """Test getting user profile."""
        response = client.get(
            "/api/profile",
            headers=auth_header
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
    
    def test_update_profile_username(self, auth_header):
        """Test updating username."""
        response = client.put(
            "/api/profile",
            json={"username": "newusername"},
            headers=auth_header
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newusername"
        
        # Verify the update persisted
        get_response = client.get(
            "/api/profile",
            headers=auth_header
        )
        assert get_response.json()["username"] == "newusername"
    
    def test_update_profile_email(self, auth_header):
        """Test updating email."""
        response = client.put(
            "/api/profile",
            json={"email": "newemail@example.com"},
            headers=auth_header
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newemail@example.com"
    
    def test_change_password_success(self, auth_header):
        """Test successful password change."""
        response = client.post(
            "/api/profile/change-password",
            json={
                "old_password": "testpass123",
                "new_password": "newpass456",
                "confirm_password": "newpass456"
            },
            headers=auth_header
        )
        assert response.status_code == 200
        
        # Verify new password works for login
        login_response = client.post(
            "/api/auth/login",
            json={
                "username": "testuser",
                "password": "newpass456"
            }
        )
        assert login_response.status_code == 200
    
    def test_change_password_old_incorrect(self, auth_header):
        """Test password change fails with incorrect old password."""
        response = client.post(
            "/api/profile/change-password",
            json={
                "old_password": "wrongoldpass",
                "new_password": "newpass456",
                "confirm_password": "newpass456"
            },
            headers=auth_header
        )
        assert response.status_code == 401
    
    def test_change_password_mismatch(self, auth_header):
        """Test password change fails when new passwords don't match."""
        response = client.post(
            "/api/profile/change-password",
            json={
                "old_password": "testpass123",
                "new_password": "newpass456",
                "confirm_password": "different789"
            },
            headers=auth_header
        )
        assert response.status_code == 400
    
    def test_unauthorized_access(self):
        """Test that endpoints require authentication."""
        response = client.get("/api/profile")
        assert response.status_code == 401

    def test_delete_account_success(self, auth_header):
        """Test successful account deletion."""
        # Delete account
        response = client.delete(
            "/api/account",
            headers=auth_header
        )
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
        
        # Verify account is deleted (login should fail)
        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "TestPass123"}
        )
        assert login_response.status_code == 401

class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
