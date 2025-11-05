"""
Database Testing Script

Tests database connectivity, model operations, and session management.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import text
from app.db.session import SessionLocal, check_db_connection
from app.db.models.user import User
from passlib.context import CryptContext


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_connection():
    """Test database connection."""
    print("\n" + "=" * 60)
    print(" Testing Database Connection")
    print("=" * 60)
    
    if check_db_connection():
        print("✅ Database connection successful!")
        return True
    else:
        print("❌ Database connection failed!")
        return False


def test_raw_query():
    """Test raw SQL query."""
    print("\n" + "=" * 60)
    print(" Testing Raw SQL Query")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"✅ PostgreSQL Version: {version}")
    except Exception as e:
        print(f"❌ Query failed: {e}")
    finally:
        db.close()


def test_create_user():
    """Test creating a user."""
    print("\n" + "=" * 60)
    print(" Testing User Creation")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        # Create test user
        test_user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=pwd_context.hash("password123"),
            is_active=True,
            is_superuser=False
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"✅ User created: {test_user}")
        print(f"   ID: {test_user.id}")
        print(f"   Email: {test_user.email}")
        print(f"   Username: {test_user.username}")
        print(f"   Created at: {test_user.created_at}")
        
        return test_user.id
        
    except Exception as e:
        db.rollback()
        print(f"❌ User creation failed: {e}")
        return None
    finally:
        db.close()


def test_read_user(user_id: int):
    """Test reading a user."""
    print("\n" + "=" * 60)
    print(" Testing User Read")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            print(f"✅ User found: {user}")
            print(f"   Email: {user.email}")
            print(f"   Is Active: {user.is_active}")
        else:
            print(f"❌ User with ID {user_id} not found")
    except Exception as e:
        print(f"❌ Read failed: {e}")
    finally:
        db.close()


def test_update_user(user_id: int):
    """Test updating a user."""
    print("\n" + "=" * 60)
    print(" Testing User Update")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            print(f"Before update: is_superuser = {user.is_superuser}")
            
            # Update user
            user.is_superuser = True
            db.commit()
            db.refresh(user)
            
            print(f"After update: is_superuser = {user.is_superuser}")
            print(f"✅ User updated successfully!")
        else:
            print(f"❌ User with ID {user_id} not found")
    except Exception as e:
        db.rollback()
        print(f"❌ Update failed: {e}")
    finally:
        db.close()


def test_list_all_users():
    """Test listing all users."""
    print("\n" + "=" * 60)
    print(" Testing List All Users")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"✅ Found {len(users)} user(s):")
        for user in users:
            print(f"   - {user.username} ({user.email})")
    except Exception as e:
        print(f"❌ List failed: {e}")
    finally:
        db.close()


def test_delete_user(user_id: int):
    """Test deleting a user."""
    print("\n" + "=" * 60)
    print(" Testing User Delete")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            username = user.username
            db.delete(user)
            db.commit()
            print(f"✅ User '{username}' deleted successfully!")
        else:
            print(f"❌ User with ID {user_id} not found")
    except Exception as e:
        db.rollback()
        print(f"❌ Delete failed: {e}")
    finally:
        db.close()


def cleanup_test_data():
    """Clean up all test data."""
    print("\n" + "=" * 60)
    print(" Cleaning Up Test Data")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        # Delete all users
        deleted = db.query(User).delete()
        db.commit()
        print(f"✅ Deleted {deleted} user(s)")
    except Exception as e:
        db.rollback()
        print(f"❌ Cleanup failed: {e}")
    finally:
        db.close()


def run_all_tests():
    """Run all database tests."""
    print("\n" + "🚀" * 30)
    print("   DATABASE TESTING SUITE")
    print("🚀" * 30)
    
    # Test 1: Connection
    if not test_connection():
        print("\n❌ Cannot proceed - database not connected")
        return
    
    # Test 2: Raw query
    test_raw_query()
    
    # Test 3: Create user
    user_id = test_create_user()
    if not user_id:
        print("\n❌ Cannot proceed - user creation failed")
        return
    
    # Test 4: Read user
    test_read_user(user_id)
    
    # Test 5: Update user
    test_update_user(user_id)
    
    # Test 6: List all users
    test_list_all_users()
    
    # Test 7: Delete user
    test_delete_user(user_id)
    
    # Verify deletion
    test_list_all_users()
    
    # Summary
    print("\n" + "=" * 60)
    print(" Test Summary")
    print("=" * 60)
    print("✅ All database tests completed!")
    print("\nNext steps:")
    print("1. Integrate database with FastAPI endpoints")
    print("2. Create user authentication")
    print("3. Build CRUD operations")


if __name__ == "__main__":
    # Install passlib if not already installed
    try:
        from passlib.context import CryptContext
    except ImportError:
        print("Installing passlib...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "passlib[bcrypt]"])
        from passlib.context import CryptContext
    
    run_all_tests()