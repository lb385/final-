import pytest
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
import subprocess
import time
import os

BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def browser():
    """Create browser instance for the test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture
def page(browser: Browser):
    """Create a new page for each test."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()

class TestUserProfileFlow:
    """E2E tests for user profile and password change flow."""
    
    def test_register_login_update_profile(self, page: Page):
        """Test full flow: register -> login -> update profile."""
        # Visit registration page
        page.goto(f"{BASE_URL}/register")
        page.wait_for_url("**/register")
        
        # Fill registration form
        page.fill('input[name="username"]', "e2euser")
        page.fill('input[name="email"]', "e2e@example.com")
        page.fill('input[name="password"]', "TestPass123")
        page.click('button[type="submit"]')
        
        # Wait for redirect to login
        page.wait_for_url("**/login", timeout=5000)
        
        # Fill login form
        page.fill('input[name="username"]', "e2euser")
        page.fill('input[name="password"]', "TestPass123")
        page.click('button[type="submit"]')
        
        # Wait for redirect to dashboard
        page.wait_for_url("**/dashboard", timeout=5000)
        
        # Navigate to profile
        page.click('a[href="/profile"]')
        page.wait_for_url("**/profile", timeout=5000)
        
        # Verify profile data
        username_value = page.input_value('input[name="username"]')
        email_value = page.input_value('input[name="email"]')
        
        assert username_value == "e2euser"
        assert email_value == "e2e@example.com"
    
    def test_change_password_flow(self, page: Page):
        """Test password change workflow."""
        # Register and login first
        page.goto(f"{BASE_URL}/register")
        page.fill('input[name="username"]', "pwduser")
        page.fill('input[name="email"]', "pwd@example.com")
        page.fill('input[name="password"]', "InitialPass123")
        page.click('button[type="submit"]')
        
        page.wait_for_url("**/login", timeout=5000)
        page.fill('input[name="username"]', "pwduser")
        page.fill('input[name="password"]', "InitialPass123")
        page.click('button[type="submit"]')
        
        page.wait_for_url("**/dashboard", timeout=5000)
        
        # Navigate to profile
        page.click('a[href="/profile"]')
        page.wait_for_url("**/profile", timeout=5000)
        
        # Click on change password section
        page.click('button:has-text("Change Password")')
        
        # Fill password change form
        page.fill('input[name="oldPassword"]', "InitialPass123")
        page.fill('input[name="newPassword"]', "NewPass456")
        page.fill('input[name="confirmPassword"]', "NewPass456")
        page.click('button:has-text("Update Password")')
        
        # Wait for success message
        page.wait_for_selector('text=Password changed successfully', timeout=5000)
        
        # Logout and login with new password
        page.click('button:has-text("Logout")')
        page.wait_for_url("**/login", timeout=5000)
        
        page.fill('input[name="username"]', "pwduser")
        page.fill('input[name="password"]', "NewPass456")
        page.click('button[type="submit"]')
        
        # Should successfully login
        page.wait_for_url("**/dashboard", timeout=5000)
    
    def test_update_email_flow(self, page: Page):
        """Test email update workflow."""
        # Register and login
        page.goto(f"{BASE_URL}/register")
        page.fill('input[name="username"]', "emailuser")
        page.fill('input[name="email"]', "old@example.com")
        page.fill('input[name="password"]', "TestPass123")
        page.click('button[type="submit"]')
        
        page.wait_for_url("**/login", timeout=5000)
        page.fill('input[name="username"]', "emailuser")
        page.fill('input[name="password"]', "TestPass123")
        page.click('button[type="submit"]')
        
        page.wait_for_url("**/dashboard", timeout=5000)
        
        # Go to profile and update email
        page.click('a[href="/profile"]')
        page.wait_for_url("**/profile", timeout=5000)
        
        page.clear('input[name="email"]')
        page.fill('input[name="email"]', "new@example.com")
        page.click('button:has-text("Save Profile")')
        
        # Wait for success
        page.wait_for_selector('text=Profile updated successfully', timeout=5000)
        
        # Verify new email is displayed
        email_value = page.input_value('input[name="email"]')
        assert email_value == "new@example.com"
    
    def test_invalid_password_change(self, page: Page):
        """Test error handling for invalid password changes."""
        # Register and login
        page.goto(f"{BASE_URL}/register")
        page.fill('input[name="username"]', "invalidpwd")
        page.fill('input[name="email"]', "inv@example.com")
        page.fill('input[name="password"]', "ValidPass123")
        page.click('button[type="submit"]')
        
        page.wait_for_url("**/login", timeout=5000)
        page.fill('input[name="username"]', "invalidpwd")
        page.fill('input[name="password"]', "ValidPass123")
        page.click('button[type="submit"]')
        
        page.wait_for_url("**/dashboard", timeout=5000)
        
        # Try to change password with wrong old password
        page.click('a[href="/profile"]')
        page.wait_for_url("**/profile", timeout=5000)
        
        page.click('button:has-text("Change Password")')
        page.fill('input[name="oldPassword"]', "WrongPass")
        page.fill('input[name="newPassword"]', "NewPass123")
        page.fill('input[name="confirmPassword"]', "NewPass123")
        page.click('button:has-text("Update Password")')
        
        # Should show error
        page.wait_for_selector('text=Old password is incorrect', timeout=5000)
    
    def test_duplicate_username_error(self, page: Page):
        """Test duplicate username detection."""
        # Create first user
        page.goto(f"{BASE_URL}/register")
        page.fill('input[name="username"]', "duplicateuser")
        page.fill('input[name="email"]', "dup1@example.com")
        page.fill('input[name="password"]', "TestPass123")
        page.click('button[type="submit"]')
        
        page.wait_for_url("**/login", timeout=5000)
        
        # Try to register with same username
        page.goto(f"{BASE_URL}/register")
        page.fill('input[name="username"]', "duplicateuser")
        page.fill('input[name="email"]', "dup2@example.com")
        page.fill('input[name="password"]', "TestPass123")
        page.click('button[type="submit"]')
        
        # Should show error
        page.wait_for_selector('text=Username or email already registered', timeout=5000)
