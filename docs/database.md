# Database Documentation

## Schema Overview

### Users Table

Stores user authentication and profile information.

**Columns:**
- `id` (INTEGER, PRIMARY KEY): Unique user identifier
- `email` (VARCHAR(255), UNIQUE): User email address
- `username` (VARCHAR(50), UNIQUE): Username for login
- `hashed_password` (VARCHAR(255)): Bcrypt hashed password
- `is_active` (BOOLEAN): Account active status
- `is_superuser` (BOOLEAN): Admin privileges flag
- `created_at` (TIMESTAMP): Account creation time
- `updated_at` (TIMESTAMP): Last update time

**Indexes:**
- Primary key on `id`
- Unique index on `email`
- Unique index on `username`

**Example Query:**
```sql
SELECT id, email, username, is_active 
FROM users 
WHERE is_active = true 
ORDER BY created_at DESC;
```

## Connection Pooling

The application uses SQLAlchemy's connection pooling:

- **Pool Size**: 5 connections (configurable)
- **Max Overflow**: 10 additional connections when needed
- **Pool Recycle**: Connections recycled after 3600 seconds
- **Pool Pre-ping**: Connections tested before use

## Migrations

### Creating a Migration
```bash
# 1. Modify model in app/db/models/
# 2. Generate migration
alembic revision --autogenerate -m "add column X to table Y"
# 3. Review generated migration in alembic/versions/
# 4. Apply migration
alembic upgrade head
```

### Rolling Back
```bash
# Rollback last migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>

# Rollback all
alembic downgrade base
```

## Best Practices

### Model Design
- Always use `nullable=False` for required fields
- Add indexes on frequently queried columns
- Use appropriate data types (don't use TEXT when VARCHAR(50) suffices)
- Add timestamps (created_at, updated_at) to all tables
- Use meaningful column names and comments

### Session Management
- Always use context managers or dependency injection
- Never commit inside loops (batch operations instead)
- Handle exceptions and rollback on errors
- Close sessions after use

### Performance
- Use eager loading for relationships (avoid N+1 queries)
- Add database indexes for WHERE/JOIN columns
- Use pagination for large result sets
- Monitor slow queries with DB_ECHO=True in development

### Security
- Never store plain text passwords
- Use parameterized queries (SQLAlchemy does this automatically)
- Validate input data with Pydantic
- Use proper access controls (is_active, is_superuser)

## Troubleshooting

### Connection Issues

**Problem:** Can't connect to database
```
Solution:
1. Check Docker is running: docker ps
2. Check database logs: docker-compose logs postgres
3. Verify DATABASE_URL in .env matches docker-compose.yml
4. Test connection: python -m app.db.test_db
```

### Migration Issues

**Problem:** Migration fails
```
Solution:
1. Check migration file for errors
2. Ensure models are imported in alembic/env.py
3. Rollback and try again: alembic downgrade -1
4. Manual fix: Access database and fix manually, then stamp:
   alembic stamp head
```

### Performance Issues

**Problem:** Slow queries
```
Solution:
1. Enable query logging: DB_ECHO=True
2. Check for N+1 queries
3. Add appropriate indexes
4. Use EXPLAIN ANALYZE in PostgreSQL
```