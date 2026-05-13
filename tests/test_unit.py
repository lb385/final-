import pytest
from backend.security import hash_password, verify_password, create_access_token, verify_token

class TestPasswordHashing:
    """Test password hashing and verification."""
    
    def test_hash_password_creates_hash(self):
        """Test that hash_password creates a hash."""
        password = "testpassword123"
        hashed = hash_password(password)
        assert hashed != password
        assert len(hashed) > 0
    
    def test_verify_password_correct(self):
        """Test that verify_password works with correct password."""
        password = "testpassword123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test that verify_password fails with incorrect password."""
        password = "testpassword123"
        wrong_password = "wrongpassword456"
        hashed = hash_password(password)
        assert verify_password(wrong_password, hashed) is False
    
    def test_hash_password_different_hashes(self):
        """Test that same password produces different hashes."""
        password = "testpassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        assert hash1 != hash2

class TestTokenManagement:
    """Test JWT token creation and verification."""
    
    def test_create_access_token(self):
        """Test that create_access_token creates a valid token."""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        assert token is not None
        assert isinstance(token, str)
    
    def test_verify_token_valid(self):
        """Test that verify_token works with valid token."""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        verified = verify_token(token)
        assert verified is not None
        assert verified.get("sub") == "testuser"
    
    def test_verify_token_invalid(self):
        """Test that verify_token fails with invalid token."""
        invalid_token = "invalid.token.here"
        verified = verify_token(invalid_token)
        assert verified is None
    
    def test_verify_token_tampered(self):
        """Test that verify_token fails with tampered token."""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        tampered = token[:-5] + "XXXXX"
        verified = verify_token(tampered)
        assert verified is None
