# Job Portal Backend API

A production-level Job Portal Backend API built with Django REST Framework, featuring JWT authentication, role-based access control, and complete hiring workflow management.

## Features

- **User Authentication**: JWT-based auth with role-based access (Candidate/Recruiter/Admin)
- **Job Management**: Post, search, and manage job listings
- **Application Tracking**: Complete application lifecycle management
- **Interview Scheduling**: Schedule and manage interviews
- **Resume Management**: Upload and manage candidate resumes
- **Background Tasks**: Celery + Redis for async operations
- **API Architecture**: Production-ready REST API design
- **Deployment Ready**: Docker, PostgreSQL, Nginx, Gunicorn setup

## Tech Stack

- **Backend**: Django 6.0.4, Django REST Framework
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Cache & Task Queue**: Redis, Celery
- **Authentication**: JWT (django-rest-framework-simplejwt)
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx, Gunicorn

## Project Structure

```
├── accounts/          # User authentication & profiles
├── jobs/              # Job posting management
├── applications/      # Job applications
├── interviews/        # Interview scheduling
├── config/            # Django configuration
├── templates/         # HTML templates
├── static/            # CSS, JavaScript
├── docker-compose.yml # Container orchestration
└── requirements.txt   # Python dependencies
```

## Setup

### Local Development

1. Clone the repository
```bash
git clone https://github.com/JAY-822005/job-portal-backend-
cd job-portal-backend-
```

2. Create virtual environment
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Start development server
```bash
python manage.py runserver
```

### Docker Setup

```bash
docker-compose up --build
```

Access the API at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/refresh/` - Refresh JWT token

### Jobs
- `GET /api/jobs/` - List all jobs
- `POST /api/jobs/` - Create job (Recruiter)
- `GET /api/jobs/{id}/` - Job details
- `PUT /api/jobs/{id}/` - Update job
- `DELETE /api/jobs/{id}/` - Delete job

### Applications
- `GET /api/applications/` - List applications
- `POST /api/applications/` - Apply for job
- `GET /api/applications/{id}/` - Application details
- `PUT /api/applications/{id}/` - Update application status

### Interviews
- `GET /api/interviews/` - List interviews
- `POST /api/interviews/` - Schedule interview
- `PUT /api/interviews/{id}/` - Update interview

## Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
```

For production, use environment-specific settings in `config/` directory.

## Testing

Run tests with pytest:
```bash
pytest
```

## Database Models

- **User**: Custom user with roles (candidate, recruiter, admin)
- **CandidateProfile**: Candidate details, skills, experience, resume
- **RecruiterProfile**: Company information, recruiter details
- **Job**: Job listings with details, salary, location
- **JobApplication**: Application tracking with status
- **Interview**: Interview scheduling and feedback

## Key Features

### Role-Based Access Control
Different permissions for Candidates, Recruiters, and Admins
- Candidates can browse jobs and apply
- Recruiters can post jobs and manage applications
- Admins have full system access

### JWT Authentication
- Access token with refresh token rotation
- Secure token management in headers
- Automatic token refresh on expiration

### Async Task Processing
- Email notifications via Celery
- Background job processing
- Scheduled tasks with Celery Beat

## Deployment

See Docker setup above for containerized deployment.

For production deployment:
1. Use `settings_prod.py` configuration
2. Set `DEBUG=False`
3. Configure PostgreSQL database
4. Use environment variables for secrets
5. Set up Redis for caching and task queue

## License

MIT

## Author

[Your Name]
