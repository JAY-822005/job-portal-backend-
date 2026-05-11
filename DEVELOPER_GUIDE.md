# 🏗️ Developer's Guide - Job Portal Backend API

## Architecture Overview

This project follows Django best practices with a **modular architecture** designed for scalability and maintainability.

### Architectural Principles

1. **Separation of Concerns** - Each app has specific responsibility
2. **DRY (Don't Repeat Yourself)** - Reusable serializers, permissions, utilities
3. **Loose Coupling** - Apps are independent and can be extended
4. **Testability** - Clear interfaces make testing straightforward
5. **Scalability** - Async tasks, caching, and database optimization

### Application Architecture

```
┌─────────────────────────────────────────┐
│         Frontend (HTML/CSS/JS)          │
├─────────────────────────────────────────┤
│      REST API (Django REST Framework)   │
├─────────────────────────────────────────┤
│  ┌───────────────────────────────────┐  │
│  │  Core Applications (accounts,     │  │
│  │  jobs, applications, interviews)  │  │
│  └───────────────────────────────────┘  │
├─────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐             │
│  │PostgreSQL│  │  Redis   │  (External) │
│  │Database  │  │  Cache   │             │
│  └──────────┘  └──────────┘             │
├─────────────────────────────────────────┤
│    Celery (Async Tasks & Scheduler)     │
└─────────────────────────────────────────┘
```

---

## 📱 Application Modules

### 1. **accounts** - User Management
**Responsibility**: User authentication, profiles, account management

**Key Models:**
- `User` - Extended Django user with roles
- `CandidateProfile` - Candidate-specific data
- `RecruiterProfile` - Company/recruiter data

**Key Endpoints:**
```
POST   /api/auth/register/          - Register new user
POST   /api/auth/login/             - User login
POST   /api/auth/token/refresh/     - Refresh JWT
GET    /api/auth/user/              - Get current user
PATCH  /api/accounts/profile/       - Update profile
```

**Permission Classes:**
- `IsAuthenticated` - User must be logged in
- `IsCandidate` - User must have candidate role
- `IsRecruiter` - User must have recruiter role

### 2. **jobs** - Job Listings
**Responsibility**: Job posting, management, and discovery

**Key Models:**
- `Job` - Job listing with full details
- `JobCategory` - Organization and filtering
- `Skill` - Skill tags

**Key Endpoints:**
```
GET    /api/jobs/                   - List all jobs
POST   /api/jobs/                   - Create job (recruiter)
GET    /api/jobs/{id}/              - Get job details
PATCH  /api/jobs/{id}/              - Update job
DELETE /api/jobs/{id}/              - Delete job
GET    /api/jobs/?location=...      - Filter jobs
```

**Features:**
- Full-text search
- Advanced filtering (location, salary, experience level)
- Pagination
- View tracking

### 3. **applications** - Job Applications
**Responsibility**: Track candidate applications and hiring pipeline

**Key Models:**
- `JobApplication` - Application record
- `ApplicationRejection` - Rejection details

**Key Endpoints:**
```
GET    /api/applications/           - List applications
POST   /api/applications/           - Submit application
GET    /api/applications/{id}/      - Get details
PATCH  /api/applications/{id}/      - Update status
```

**Status Workflow:**
```
Applied → Under Review → Shortlisted → Interviewed → Hired
                      ↓
                   Rejected (with reason)
```

### 4. **interviews** - Interview Management
**Responsibility**: Schedule and track interviews

**Key Models:**
- `Interview` - Interview details and status
- `InterviewFeedback` - Structured feedback
- `InterviewScheduleTemplate` - Reusable templates

**Key Endpoints:**
```
GET    /api/interviews/             - List interviews
POST   /api/interviews/             - Schedule interview
PATCH  /api/interviews/{id}/        - Update interview
POST   /api/interviews/{id}/feedback/ - Add feedback
```

---

## 🔐 Permission & Authentication Flow

### User Roles

```
┌─────────────────────────────────────────────┐
│          User                               │
├─────────────────────────────────────────────┤
│  Role (Candidate/Recruiter/Admin)           │
│  is_verified (Email verification status)    │
│  Profile (CandidateProfile/RecruiterProfile)│
└─────────────────────────────────────────────┘
```

### Authentication Flow

```
User Registration/Login
        ↓
Generate JWT Tokens (Access + Refresh)
        ↓
Client stores tokens in localStorage
        ↓
Client includes token in API requests
        ↓
Server validates token
        ↓
Check user role-based permissions
        ↓
Execute request or return 403 Forbidden
```

### Permission Hierarchy

```
Public endpoints (no auth required)
        ↓
Authenticated endpoints (@permission_classes([IsAuthenticated]))
        ↓
Role-specific endpoints (@permission_classes([IsCandidate|IsRecruiter]))
        ↓
Admin-only endpoints (@permission_classes([IsAdmin]))
```

---

## 🗄️ Database Schema Overview

### Key Relationships

```
User (1) ──────── (1) CandidateProfile
User (1) ──────── (1) RecruiterProfile

RecruiterProfile (1) ──────── (N) Job
Job (1) ──────---- (N) JobApplication
CandidateProfile (1) ──────---- (N) JobApplication

JobApplication (1) ──────---- (1) Interview
```

### Indexing Strategy

Indexed fields for optimal query performance:
- `User.email` - Frequent lookups
- `Job.recruiter + status` - Complex filters
- `JobApplication.job + status` - Pipeline tracking
- `Interview.status + scheduled_at` - Schedule queries

---

## 🔄 API Response Format

### Success Response
```json
{
    "success": true,
    "data": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    },
    "message": "Operation successful"
}
```

### Error Response
```json
{
    "success": false,
    "error": {
        "detail": "Invalid credentials."
    },
    "message": "An error occurred",
    "status_code": 401
}
```

### Paginated Response
```json
{
    "count": 100,
    "next": "http://api.example.com/api/jobs/?page=2",
    "previous": null,
    "results": [...]
}
```

---

## 🧪 Testing Strategy

### Test Structure
```
tests/
├── test_auth.py          - Authentication tests
├── test_jobs.py          - Job management tests
├── test_applications.py  - Application tests
└── test_interviews.py    - Interview tests
```

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=.

# Specific test file
pytest tests/test_auth.py

# Specific test function
pytest tests/test_auth.py::TestUserRegistration::test_valid_registration
```

### Test Example
```python
def test_job_creation(client, recruiter_user):
    """Test that recruiter can create job"""
    client.force_authenticate(user=recruiter_user)
    response = client.post('/api/jobs/', {
        'title': 'Senior Developer',
        'description': 'We are looking for...',
        'location': 'San Francisco',
        'salary_min': 100000,
        'salary_max': 150000,
    })
    assert response.status_code == 201
    assert response.data['title'] == 'Senior Developer'
```

---

## 🔧 Extending the Application

### Adding a New Feature

1. **Create Django App**
```bash
python manage.py startapp feature_name
```

2. **Define Models** (models.py)
```python
from django.db import models
from accounts.models import User

class Feature(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
```

3. **Create Serializer** (serializers.py)
```python
from rest_framework import serializers
from .models import Feature

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ('id', 'title', 'user', 'created_at')
        read_only_fields = ('id', 'created_at')
```

4. **Create ViewSet** (views.py)
```python
from rest_framework.viewsets import ModelViewSet
from .models import Feature
from .serializers import FeatureSerializer

class FeatureViewSet(ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
```

5. **Register URLs** (urls.py)
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeatureViewSet

router = DefaultRouter()
router.register(r'features', FeatureViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

6. **Run Migrations**
```bash
python manage.py makemigrations feature_name
python manage.py migrate
```

---

## 📧 Async Tasks

### Creating a Celery Task

```python
# features/tasks.py
from celery import shared_task
from .models import Feature

@shared_task
def process_feature(feature_id):
    try:
        feature = Feature.objects.get(id=feature_id)
        # Do expensive operation
        return f"Processed feature {feature_id}"
    except Feature.DoesNotExist:
        return f"Feature {feature_id} not found"
```

### Calling from View

```python
from .tasks import process_feature

def create_feature(request):
    feature = Feature.objects.create(...)
    # Queue task
    process_feature.delay(feature.id)
    return Response({"status": "processing"})
```

### Scheduled Tasks

Add to `config/celery.py`:
```python
'beat_schedule': {
    'process-features': {
        'task': 'features.tasks.process_feature',
        'schedule': 3600.0,  # Every hour
    },
}
```

---

## 🎯 Code Quality Standards

### Code Style
```bash
# Format with Black
black .

# Sort imports
isort .

# Check style
flake8 .
```

### Naming Conventions
- **Models**: Singular, PascalCase (`User`, `JobApplication`)
- **Variables**: snake_case (`user_name`, `job_title`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRIES`, `DEFAULT_TIMEOUT`)
- **Methods**: snake_case, verb-based (`get_user()`, `create_job()`)

### Documentation
```python
def get_user_jobs(user_id: int) -> QuerySet:
    """
    Get all active jobs posted by a user.
    
    Args:
        user_id: The ID of the recruiter user
        
    Returns:
        QuerySet of active Job objects
        
    Raises:
        User.DoesNotExist: If user not found
    """
    user = User.objects.get(id=user_id)
    return Job.objects.filter(recruiter__user=user, is_active=True)
```

---

## 🐛 Debugging Tips

### Django Shell
```bash
python manage.py shell

# Query database
User.objects.filter(role='candidate').count()

# Create test data
user = User.objects.create_user(username='test', email='test@example.com', password='pass')
```

### Print Debug Info
```python
import logging
logger = logging.getLogger(__name__)

logger.debug(f"User: {user}")
logger.info(f"Job created: {job.id}")
logger.error(f"Error: {str(e)}")
```

### Check Logs
```bash
# Django logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f web

# Celery logs
docker-compose logs -f celery
```

---

## 📊 Performance Monitoring

### Database Queries
```python
from django.db import connection
from django.test.utils import override_settings

@override_settings(DEBUG=True)
def check_queries():
    # Your code here
    print(f"Queries: {len(connection.queries)}")
```

### Query Optimization
```python
# Bad: N+1 queries
jobs = Job.objects.all()
for job in jobs:
    print(job.recruiter.company_name)  # N queries

# Good: Prefetch related
jobs = Job.objects.select_related('recruiter')
for job in jobs:
    print(job.recruiter.company_name)  # 1 query
```

---

## 🚀 Deployment Notes

### Pre-deployment Checklist
- [ ] Run tests: `pytest`
- [ ] Check code quality: `flake8`
- [ ] Format code: `black`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect static: `python manage.py collectstatic`
- [ ] Check settings: `python manage.py check --deploy`

### Environment Variables
All sensitive data should be in `.env`:
- SECRET_KEY
- Database credentials
- API keys
- Email credentials
- Redis URL

---

## 📚 Useful Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Redis Docs](https://redis.io/documentation)

---

## 💡 Best Practices

1. **Always use transactions for related operations**
```python
from django.db import transaction

@transaction.atomic
def create_job_and_notify():
    job = Job.objects.create(...)
    notify_recruiters.delay()
```

2. **Use select_related/prefetch_related**
```python
# Optimize queries
jobs = Job.objects.select_related('recruiter').prefetch_related('applications')
```

3. **Implement proper error handling**
```python
try:
    user = User.objects.get(id=user_id)
except User.DoesNotExist:
    return Response({'error': 'User not found'}, status=404)
```

4. **Use pagination for list endpoints**
```python
class JobViewSet(ModelViewSet):
    pagination_class = PageNumberPagination
```

5. **Add appropriate logging**
```python
logger.info(f"User {user.id} logged in")
logger.error(f"Failed to send email: {str(e)}")
```

---

**Happy coding! 🚀**
