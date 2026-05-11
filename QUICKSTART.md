# Quick Start Guide

## Setup (5 minutes)

### Clone & Install
```bash
git clone https://github.com/JAY-822005/job-portal-backend-
cd job-portal-backend-
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env (optional for basic development)
# For PostgreSQL, update database credentials
```

### Step 3: Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata sample_data.json
```

### Step 4: Run Development Server

```bash
# Start Django development server
python manage.py runserver

# In another terminal, start Celery (optional for async tasks)
celery -A config worker -l info
```

Access the application:
- **Web Interface**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Docs**: http://localhost:8000/api/docs/

## 🔐 First User Login

1. Go to `/register` to create an account
2. Choose your role:
   - **Job Seeker** - Apply for jobs, track applications
   - **Recruiter** - Post jobs, review applications
3. Complete your profile
4. Browse or post jobs

## 📚 Key URLs

### User Features
- **Homepage**: `/`
- **Register**: `/register`
- **Login**: `/login`
- **Dashboard**: `/dashboard`
- **Browse Jobs**: `/jobs`
- **Applications**: `/applications`

### API Endpoints
- **API Root**: `/api/`
- **Swagger Docs**: `/api/docs/`
- **ReDoc**: `/api/redoc/`

### Admin
- **Admin Panel**: `/admin`

## 🔑 Common API Operations

### Register a New User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "role": "candidate"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Browse Jobs
```bash
curl http://localhost:8000/api/jobs/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Apply for a Job
```bash
curl -X POST http://localhost:8000/api/applications/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "job": 1,
    "cover_letter": "I am very interested in this position..."
  }'
```

## 🐳 Docker Quickstart

```bash
# Build and start services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

## 📁 Project Structure Overview

```
├── accounts/          # User authentication
├── jobs/              # Job listings
├── applications/      # Job applications
├── interviews/        # Interview scheduling
├── config/            # Project configuration
├── templates/         # HTML templates
├── static/            # CSS, JavaScript, images
├── manage.py          # Django CLI
└── requirements_production.txt  # Dependencies
```

## 🧪 Run Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_auth.py

# With coverage
pytest --cov=.
```

## 🛠️ Common Commands

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run shell
python manage.py shell

# Create sample data
python manage.py shell < scripts/create_sample_data.py
```

## 🔧 Development Tips

### Hot Reload with Watchdog
```bash
pip install django-extensions
python manage.py runserver_plus
```

### Database Shell
```bash
# PostgreSQL
python manage.py dbshell

# Execute migrations
python manage.py migrate
```

### Check Environment
```bash
# Verify configuration
python manage.py check

# Show installed apps
python manage.py shell -c "from django.conf import settings; print(settings.INSTALLED_APPS)"
```

## ⚠️ Common Issues

### Database Connection Error
- Ensure PostgreSQL is running
- Check credentials in `.env`
- Verify database exists: `createdb job_portal`

### Redis Connection Error
- Start Redis: `redis-server`
- Check Redis URL in `.env`

### Static Files Missing
- Run: `python manage.py collectstatic`

### Port Already in Use
- Change port: `python manage.py runserver 8001`

## 📖 Next Steps

1. **Update Profile**: Complete your candidate/recruiter profile
2. **Explore API**: Visit `/api/docs` for interactive documentation
3. **Post/Apply**: Try posting a job or applying for one
4. **Schedule Interview**: Test interview scheduling feature
5. **Check Dashboard**: View analytics and application status

## 🤝 Need Help?

- **Documentation**: Check `README_NEW.md`
- **API Docs**: Visit `/api/docs`
- **Issues**: Open a GitHub issue
- **Email**: support@jobportal.com

---

**Happy coding! 🚀**
