# 🚀 DataPipeline Pro

> A production-grade real-time data processing and analytics platform

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

## 📋 Overview

DataPipeline Pro is a scalable, event-driven data processing platform designed to ingest, process, and analyze high-volume data streams in real-time. Built with modern Python frameworks and cloud-native technologies, it demonstrates production-ready practices for backend and data engineering.

### 🎯 Key Features (Planned)

- **Real-time Data Ingestion** - RESTful APIs for high-throughput data ingestion
- **Stream Processing** - Event-driven architecture using Apache Kafka
- **Data Transformation** - Automated ETL pipelines with Apache Airflow and dbt
- **Analytics Dashboard** - Interactive visualization with Streamlit
- **Production Monitoring** - Comprehensive observability with Prometheus & Grafana
- **Data Quality** - Automated validation and testing with Great Expectations

## 🛠️ Tech Stack

### Backend & API
- **FastAPI** - Modern, async Python web framework
- **Python 3.11+** - Core programming language
- **Pydantic** - Data validation and settings management

### Data Processing
- **Apache Kafka** - Distributed event streaming platform
- **Apache Airflow** - Workflow orchestration
- **dbt** - Data transformation framework
- **Pandas** - Data manipulation and analysis

### Databases
- **PostgreSQL** - Primary relational database
- **TimescaleDB** - Time-series data extension
- **Redis** - Caching and rate limiting

### Infrastructure & DevOps
- **Docker & Docker Compose** - Containerization
- **GitHub Actions** - CI/CD pipeline
- **Prometheus & Grafana** - Monitoring and visualization
- **AWS S3** - Data lake storage

### Testing & Quality
- **pytest** - Testing framework
- **Great Expectations** - Data quality validation
- **Sentry** - Error tracking and monitoring

## 🏗️ Architecture
```
┌─────────────┐     ┌──────────┐     ┌───────────┐     ┌──────────────┐
│  Data       │────▶│  FastAPI │────▶│   Kafka   │────▶│  Stream      │
│  Sources    │     │  Gateway │     │  Topics   │     │  Processors  │
└─────────────┘     └──────────┘     └───────────┘     └──────────────┘
                                                               │
                                                               ▼
                    ┌──────────┐     ┌──────────────────────────┐
                    │ Streamlit│◀────│    PostgreSQL +          │
                    │ Dashboard│     │    TimescaleDB           │
                    └──────────┘     └──────────────────────────┘
                                                ▲
                                                │
                                      ┌─────────┴─────────┐
                                      │  Airflow + dbt    │
                                      │  (Batch ETL)      │
                                      └───────────────────┘
```

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- Docker Desktop
- Git

### Setup

1. **Clone the repository**
```bash
   git clone https://github.com/parthsheth001/datapipeline-pro.git
   cd datapipeline-pro
```

2. **Create virtual environment**
```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
   cp .env.example .env
   # Edit .env with your configuration
```

5. **Run the application**
```bash
   uvicorn app.main:app --reload
```

6. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 🚀 Quick Start

### Test the API
```bash
# Health check
curl http://localhost:8000/health

# API root
curl http://localhost:8000/
```

Expected response:
```json
{
  "message": "Welcome to DataPipeline Pro",
  "status": "running",
  "version": "0.1.0"
}
```

## 📁 Project Structure
```
datapipeline-pro/
├── app/
│   ├── api/            # API endpoints
│   ├── core/           # Core configurations
│   ├── db/             # Database models and connections
│   ├── schemas/        # Pydantic models
│   ├── services/       # Business logic
│   └── main.py         # Application entry point
├── tests/              # Test suite
├── docker/             # Docker configurations
├── docs/               # Documentation
├── .env.example        # Environment variables template
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## 🧪 Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 🐳 Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🗄️ Database

### Setup

The project uses PostgreSQL with Docker for easy setup:
```bash
# Start database
docker-compose up -d

# Stop database
docker-compose down

# View database logs
docker-compose logs -f postgres
```

### Migrations

Database schema is managed with Alembic:
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

### pgAdmin

Access database management UI at http://localhost:5050

- Email: admin@datapipeline.com
- Password: admin123

To connect to database in pgAdmin:
1. Add new server
2. Host: postgres (container name)
3. Port: 5432
4. Database: datapipeline_dev
5. Username: postgres
6. Password: (from your .env)

### Database Testing
```bash
# Run database tests
python -m app.db.test_db

# Test via API
curl http://localhost:8000/api/v1/database/health
```

## 📈 Development Roadmap

- [x] Phase 1: Project setup and FastAPI foundation
- [ ] Phase 2: Authentication and core API endpoints
- [ ] Phase 3: Kafka integration for real-time streaming
- [ ] Phase 4: Airflow ETL pipelines
- [ ] Phase 5: Data transformation with dbt
- [ ] Phase 6: Monitoring and observability
- [ ] Phase 7: Streamlit analytics dashboard
- [ ] Phase 8: Production deployment

## 🤝 Contributing

This is a personal portfolio project, but feedback and suggestions are welcome!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Parth Sheth**
- GitHub: [@parthsheth001](https://github.com/parthsheth001)
- LinkedIn: [Parth Sheth](https://linkedin.com/in/parth577)
- Email: shethparth577@gmail.com

## 🙏 Acknowledgments

Built as part of a portfolio project to demonstrate:
- Modern Python backend development
- Real-time data processing architectures
- Production-ready DevOps practices
- Data engineering best practices

---

⭐ Star this repo if you find it interesting!