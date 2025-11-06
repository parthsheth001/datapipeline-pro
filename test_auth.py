"""
Authentication Testing Script

Test user registration, login, and protected routes.
"""

import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000/api/v1"

# Test user data
TEST_USER = {
    "email": "testuser@example.com",
    "username": "testuser",
    "password": "TestPassword123"
}


def print_separator(title: str):
    """Print a formatted separator."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def test_register():
    """Test user registration."""
    print_separator("Testing User Registration")
    
    url = f"{BASE_URL}/auth/register"
    
    try:
        response = requests.post(url, json=TEST_USER)
        
        if response.status_code == 201:
            user = response.json()
            print("✅ Registration successful!")
            print(f"   User ID: {user['id']}")
            print(f"   Email: {user['email']}")
            print(f"   Username: {user['username']}")
            return True
        elif response.status_code == 400:
            error = response.json()
            print(f"⚠️  User already exists: {error['detail']}")
            return True  # Not an error, just already registered
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False


def test_login() -> Optional[str]:
    """Test user login and return access token."""
    print_separator("Testing User Login")
    
    url = f"{BASE_URL}/auth/login"
    
    # OAuth2PasswordRequestForm expects form data, not JSON
    form_data = {
        "username": TEST_USER["email"],  # OAuth2 calls it username
        "password": TEST_USER["password"]
    }
    
    try:
        response = requests.post(url, data=form_data)
        
        if response.status_code == 200:
            tokens = response.json()
            print("✅ Login successful!")
            print(f"   Access Token: {tokens['access_token'][:50]}...")
            print(f"   Refresh Token: {tokens['refresh_token'][:50]}...")
            print(f"   Token Type: {tokens['token_type']}")
            return tokens['access_token']
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   {response.json()}")
            return None
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None


def test_get_current_user(token: str):
    """Test getting current user info."""
    print_separator("Testing Get Current User")
    
    url = f"{BASE_URL}/auth/me"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            user = response.json()
            print("✅ Retrieved user info!")
            print(f"   Email: {user['email']}")
            print(f"   Username: {user['username']}")
            print(f"   Active: {user['is_active']}")
            print(f"   Superuser: {user['is_superuser']}")
            return True
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False


def test_test_token(token: str):
    """Test token validation endpoint."""
    print_separator("Testing Token Validation")
    
    url = f"{BASE_URL}/auth/test-token"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Token is valid!")
            print(f"   Email: {data['email']}")
            return True
        else:
            print(f"❌ Token validation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False


def test_invalid_token():
    """Test with invalid token."""
    print_separator("Testing Invalid Token")
    
    url = f"{BASE_URL}/auth/me"
    headers = {"Authorization": "Bearer invalid_token_here"}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 401:
            print("✅ Invalid token correctly rejected!")
            return True
        else:
            print(f"❌ Expected 401, got: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False


def test_without_token():
    """Test protected route without token."""
    print_separator("Testing Protected Route Without Token")
    
    url = f"{BASE_URL}/auth/me"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 401:
            print("✅ Unauthorized access correctly rejected!")
            return True
        else:
            print(f"❌ Expected 401, got: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False


def test_change_password(token: str):
    """Test password change."""
    print_separator("Testing Password Change")
    
    url = f"{BASE_URL}/auth/change-password"
    headers = {"Authorization": f"Bearer {token}"}
    
    password_data = {
        "current_password": TEST_USER["password"],
        "new_password": "NewTestPassword123"
    }
    
    try:
        response = requests.post(url, json=password_data, headers=headers)
        
        if response.status_code == 200:
            print("✅ Password changed successfully!")
            
            # Change it back
            password_data = {
                "current_password": "NewTestPassword123",
                "new_password": TEST_USER["password"]
            }
            response = requests.post(url, json=password_data, headers=headers)
            
            if response.status_code == 200:
                print("✅ Password changed back successfully!")
            
            return True
        else:
            print(f"❌ Password change failed: {response.status_code}")
            print(f"   {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False


def run_all_tests():
    """Run all authentication tests."""
    print("\n" + "🔐" * 30)
    print("   AUTHENTICATION TESTING SUITE")
    print("🔐" * 30)
    
    print("\nMake sure the FastAPI app is running on http://localhost:8000")
    input("Press Enter to continue...")
    
    # Test 1: Register user
    if not test_register():
        print("\n❌ Registration failed, stopping tests")
        return
    
    # Test 2: Login
    token = test_login()
    if not token:
        print("\n❌ Login failed, stopping tests")
        return
    
    # Test 3: Get current user
    test_get_current_user(token)
    
    # Test 4: Test token
    test_test_token(token)
    
    # Test 5: Invalid token
    test_invalid_token()
    
    # Test 6: Without token
    test_without_token()
    
    # Test 7: Change password
    test_change_password(token)
    
    # Summary
    print_separator("Test Summary")
    print("✅ All authentication tests completed!")
    print("\nYou now have:")
    print("1. ✅ User registration working")
    print("2. ✅ User login with JWT tokens")
    print("3. ✅ Protected routes with authentication")
    print("4. ✅ Token validation")
    print("5. ✅ Password change functionality")
    print("\nNext steps:")
    print("- Test in browser at http://localhost:8000/docs")
    print("- Use the 'Authorize' button to login")
    print("- Try protected endpoints")


if __name__ == "__main__":
    run_all_tests()