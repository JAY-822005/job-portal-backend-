# 🚀 Job Portal Backend API - Production Ready

A **production-level** Job Portal Backend API built with **Django**, **Django REST Framework**, **PostgreSQL**, **JWT Authentication**, **Celery**, **Redis**, and scalable backend architecture principles.

> This is not just a tutorial project — it's designed as a **professional portfolio project** that demonstrates industry-standard backend engineering practices.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Frontend](#frontend)
- [Deployment](#deployment)
- [Contributing](#contributing)

## 🎯 Overview

This Job Portal system simulates **real-world recruitment platforms** with complete hiring workflows between Job Seekers, Recruiters, and Admins. Unlike basic CRUD projects, this implementation focuses on:

- **Clean Architecture** - Modular app design with separation of concerns
- **Security** - JWT authentication, role-based access control, input validation
- **Scalability** - Async task processing, caching, database optimization
- **Production Ready** - Environment-based settings, logging, error handling
- **API Design** - RESTful principles, pagination, filtering, throttling
- **Database** - Optimized schema, indexes, relationships

## ✨ Key Features

### For Job Seekers (Candidates)
- ✅ User registration and profile management
- ✅ Resume upload and portfolio links
- ✅ Browse and search job listings
- ✅ Apply for jobs with cover letters
- ✅ Track application status
- ✅ Schedule and attend interviews
- ✅ View job recommendations

### For Recruiters/Employers
- ✅ Company profile management
- ✅ Post and manage job listings
- ✅ View and manage applications
- ✅ Rate and shortlist candidates
- ✅ Schedule interviews
- ✅ Track hiring pipeline
- ✅ Analytics dashboard

### For Administrators
- ✅ User management
- ✅ Content moderation
- ✅ System analytics
- ✅ Activity monitoring
- ✅ Configuration management

### Technical Features
- ✅ **JWT Authentication** with refresh token rotation
- ✅ **Role-Based Access Control** (RBAC)
- ✅ **Async Task Processing** with Celery
- ✅ **Caching** with Redis
- ✅ **Full-Text Search** capabilities
- ✅ **Pagination & Filtering**
- ✅ **Rate Limiting & Throttling**
- ✅ **Comprehensive Logging**
- ✅ **Email Notifications**
- ✅ **API Documentation** with Swagger

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 4.2
- **REST API**: Django REST Framework
- **Authentication**: JWT (SimpleJWT)
- **Database**: PostgreSQL
- **Async Tasks**: Celery + Redis
- **Caching**: Redis + Django-Redis
- **API Docs**: drf-yasg (Swagger)

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with custom properties
- **JavaScript** - Vanilla JS (no dependencies)
- **Responsive** - Mobile-first design

### DevOps & Deployment
- **Containerization**: Docker & Docker Compose
- **Server**: Gunicorn
- **Web Server**: Nginx
- **Monitoring**: Sentry

### Development Tools
- **Code Quality**: Black, Flake8, isort
- **Testing**: pytest, pytest-django
- **Documentation**: Sphinx, OpenAPI

## 📁 Project Structure

```
job-portal-backend/
├── config/                      # Project configuration
│   ├── settings_base.py        # Base settings (shared)
│   ├── settings_dev.py         # Development settings
│   ├── settings_prod.py        # Production settings
│   ├── urls.py                 # Main URL router
│   ├── permissions.py          # Custom permissions
│   ├── exceptions.py           # Custom exception handlers
│   └── utils.py                # Utility functions
│
├── accounts/                   # User authentication & profiles
│   ├── models.py              # User, CandidateProfile, RecruiterProfile
│   ├── serializers.py         # User serializers
│   ├── views.py               # Authentication views
│   └── urls.py                # Auth endpoints
│
├── jobs/                       # Job management
│   ├── models.py              # Job, JobCategory, Skill models
│   ├── serializers.py         # Job serializers
│   ├── views.py               # Job viewsets
│   ├── filters.py             # Custom filters
│   └── urls.py                # Job endpoints
│
├── applications/               # Job applications
│   ├── models.py              # JobApplication, ApplicationRejection
│   ├── serializers.py         # Application serializers
│   ├── views.py               # Application views
│   └── urls.py                # Application endpoints
│
├── interviews/                 # Interview scheduling
│   ├── models.py              # Interview, InterviewFeedback
│   ├── serializers.py         # Interview serializers
│   ├── views.py               # Interview views
│   └── urls.py                # Interview endpoints
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── jobs_list.html         # Jobs listing
│   └── dashboard.html         # User dashboard
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Main styles
│   ├── js/
│   │   └── main.js            # JavaScript utilities
│   └── images/                # Image assets
│
├── logs/                       # Application logs
│
├── .env.example               # Environment variables template
├── requirements_production.txt # Production dependencies
├── manage.py                  # Django CLI
├── docker-compose.yml         # Docker Compose setup
├── Dockerfile                 # Docker image
├── nginx.conf                 # Nginx configuration
└── README.md                  # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- Redis 6+
- Docker (optional)

### Local Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd job-portal-backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements_production.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Setup database**
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Load sample data (optional)**
```bash
python manage.py loaddata sample_data.json
```

7. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

8. **Run development server**
```bash
python manage.py runserver
```

Access the application at `http://localhost:8000`

### Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up -d

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run migrations
docker-compose exec web python manage.py migrate
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
ENVIRONMENT=development
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=job_portal
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# JWT
JWT_ACCESS_TOKEN_LIFETIME=3600
JWT_REFRESH_TOKEN_LIFETIME=604800

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Database Migrations

```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

## 📚 API Documentation

### Access API Documentation
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`

### Key API Endpoints

#### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login with email/password
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET /api/auth/user/` - Get current user

#### Jobs
- `GET /api/jobs/` - List all jobs
- `POST /api/jobs/` - Create new job (recruiter only)
- `GET /api/jobs/{id}/` - Get job details
- `PATCH /api/jobs/{id}/` - Update job
- `DELETE /api/jobs/{id}/` - Delete job

#### Applications
- `GET /api/applications/` - List applications
- `POST /api/applications/` - Apply for job
- `GET /api/applications/{id}/` - Get application details
- `PATCH /api/applications/{id}/` - Update application status

#### Interviews
- `GET /api/interviews/` - List interviews
- `POST /api/interviews/` - Schedule interview
- `PATCH /api/interviews/{id}/` - Update interview
- `POST /api/interviews/{id}/feedback/` - Add interview feedback

## 🎨 Frontend Features

### Pages Included
- **Login/Register** - User authentication
- **Home Page** - Hero section with search
- **Jobs Listing** - Browse and filter jobs
- **Dashboard** - Personalized user dashboard
- **Base Template** - Responsive layout with navigation

### Features
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ JWT token authentication
- ✅ Real-time form validation
- ✅ Dynamic content loading
- ✅ Error handling and notifications
- ✅ Modern CSS with CSS variables

## 🚢 Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in settings
- [ ] Change `SECRET_KEY` to a strong value
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure email backend (Gmail, SendGrid, etc.)
- [ ] Set up Redis for caching/Celery
- [ ] Configure static file serving (AWS S3, etc.)
- [ ] Enable HTTPS/SSL
- [ ] Set up monitoring (Sentry)
- [ ] Configure backups
- [ ] Set up CI/CD pipeline

### Docker Deployment

```bash
# Build image
docker build -t job-portal:latest .

# Push to registry
docker push your-registry/job-portal:latest

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

### Heroku Deployment

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set ENVIRONMENT=production SECRET_KEY=your-key

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## 📝 Code Quality

```bash
# Format code with Black
black .

# Check code style
flake8 .

# Sort imports
isort .
```

## 🔐 Security Features

- ✅ JWT authentication with secure token rotation
- ✅ CORS protection
- ✅ CSRF protection
- ✅ SQL injection prevention (via ORM)
- ✅ Password hashing (PBKDF2)
- ✅ Rate limiting and throttling
- ✅ Input validation and sanitization
- ✅ Secure headers (HSTS, X-Frame-Options)
- ✅ Environment-based secrets management

## 📊 Performance Optimization

- ✅ Database indexing
- ✅ Query optimization (select_related, prefetch_related)
- ✅ Redis caching
- ✅ Pagination for large datasets
- ✅ Async task processing
- ✅ CDN for static files
- ✅ Gzip compression

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 💬 Support & Contact

- **Documentation**: [Full Documentation](docs/)
- **Issues**: [GitHub Issues](issues/)
- **Email**: support@jobportal.com

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8949)
- [REST API Design](https://restfulapi.net/)

---

**Built with ❤️ for backend engineers who want to stand out**

This project demonstrates production-level backend development skills and is perfect for portfolio projects, job interviews, and learning advanced Django concepts.
