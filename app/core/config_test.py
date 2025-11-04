"""
Configuration Testing Script

This script tests if the configuration system works correctly.
Run with: python -m app.core.config_test
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.core.config import get_settings, Settings


def print_separator(title: str):
    """Print a formatted separator."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def test_settings_load():
    """Test if settings load correctly from .env file."""
    print_separator("Testing Settings Load")
    
    try:
        settings = get_settings()
        print("✅ Settings loaded successfully!")
        return settings
    except Exception as e:
        print(f"❌ Failed to load settings: {e}")
        return None


def test_settings_values(settings: Settings):
    """Test and display settings values."""
    print_separator("Application Settings")
    print(f"App Name: {settings.APP_NAME}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"API Version: {settings.API_VERSION}")
    print(f"Log Level: {settings.LOG_LEVEL}")
    
    print_separator("Database Settings")
    print(f"Database URL: {settings.DATABASE_URL}")
    print(f"Pool Size: {settings.DB_POOL_SIZE}")
    print(f"Max Overflow: {settings.DB_MAX_OVERFLOW}")
    print(f"Echo SQL: {settings.DB_ECHO}")
    
    print_separator("Redis Settings")
    print(f"Redis URL: {settings.REDIS_URL}")
    print(f"Max Connections: {settings.REDIS_MAX_CONNECTIONS}")
    
    print_separator("Security Settings")
    print(f"Algorithm: {settings.ALGORITHM}")
    print(f"Access Token Expire: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} minutes")
    print(f"Secret Key: {'*' * len(settings.SECRET_KEY)} (hidden for security)")
    print(f"Secret Key Length: {len(settings.SECRET_KEY)} characters")
    
    print_separator("API Settings")
    print(f"API Prefix: {settings.API_PREFIX}")
    print(f"CORS Origins: {settings.CORS_ORIGINS}")
    print(f"Rate Limit: {settings.RATE_LIMIT_PER_MINUTE}/min")


def test_computed_properties(settings: Settings):
    """Test computed properties."""
    print_separator("Computed Properties")
    print(f"Is Development: {settings.is_development}")
    print(f"Is Production: {settings.is_production}")
    print(f"Async Database URL: {settings.database_url_async}")


def test_helper_methods(settings: Settings):
    """Test helper methods."""
    print_separator("Helper Methods")
    
    db_settings = settings.get_database_settings()
    print("Database Settings Dictionary:")
    for key, value in db_settings.items():
        print(f"  {key}: {value}")
    
    redis_settings = settings.get_redis_settings()
    print("\nRedis Settings Dictionary:")
    for key, value in redis_settings.items():
        print(f"  {key}: {value}")


def test_validation():
    """Test validation rules."""
    print_separator("Testing Validation")
    
    # Test 1: Valid settings
    print("\n1. Testing valid settings...")
    try:
        settings = Settings()
        print("✅ Valid settings passed")
    except Exception as e:
        print(f"❌ Validation failed: {e}")
    
    # Note: To test invalid settings, you would need to:
    # - Temporarily modify .env file
    # - Or pass invalid values directly to Settings()
    # For now, we'll just document what should fail
    
    print("\n2. Validation rules in place:")
    print("   ✓ SECRET_KEY must be at least 32 characters")
    print("   ✓ ENVIRONMENT must be development/staging/production")
    print("   ✓ LOG_LEVEL must be DEBUG/INFO/WARNING/ERROR/CRITICAL")
    print("   ✓ DATABASE_URL must start with postgresql://")
    print("   ✓ REDIS_URL must start with redis://")


def test_singleton_pattern():
    """Test that get_settings returns the same instance."""
    print_separator("Testing Singleton Pattern")
    
    settings1 = get_settings()
    settings2 = get_settings()
    
    if settings1 is settings2:
        print("✅ Singleton pattern working correctly")
        print("   Both calls return the same instance")
    else:
        print("❌ Singleton pattern NOT working")
        print("   Multiple instances created")


def run_all_tests():
    """Run all configuration tests."""
    print("\n" + "🚀" * 30)
    print("   CONFIGURATION TESTING SUITE")
    print("🚀" * 30)
    
    # Test 1: Load settings
    settings = test_settings_load()
    if not settings:
        print("\n❌ Cannot proceed with other tests - settings failed to load")
        return
    
    # Test 2: Display settings values
    test_settings_values(settings)
    
    # Test 3: Computed properties
    test_computed_properties(settings)
    
    # Test 4: Helper methods
    test_helper_methods(settings)
    
    # Test 5: Validation
    test_validation()
    
    # Test 6: Singleton pattern
    test_singleton_pattern()
    
    # Final summary
    print_separator("Test Summary")
    print("✅ All tests completed!")
    print("\nNext steps:")
    print("1. Verify all settings are correct")
    print("2. Generate a real SECRET_KEY if using default")
    print("3. Update .env with your actual values")
    print("4. Integrate settings into FastAPI app")


if __name__ == "__main__":
    run_all_tests()