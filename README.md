# Multilingual FAQ Management System

A Django-based FAQ management system with automatic translation support, WYSIWYG editing, and Redis caching.

## Features

- ✨ WYSIWYG Editor (CKEditor) for rich text formatting
- 🌍 Support for multiple languages with easy extensibility
- 🌍 Automatic translation to multiple languages (Hindi, Bengali)
- 🚀 REST API with language-based filtering
- 💾 Redis caching for optimized performance
- 🔄 Automatic translation during FAQ creation
- 📝 Rich text formatting for answers
- 🎨 User-friendly admin interface
- 🔍 Language-specific content retrieval
- ⚡ Fast API responses with caching
- 🔒 Fallback to English when translation unavailable

## Tech Stack

- Django 5.1.5 (Web Framework)
- Django REST Framework (API Development)
- django-ckeditor (WYSIWYG Editor)
- Redis (Caching)
- googletrans (Translation Service)
- Docker & Docker Compose (Containerization)

## Installation

- **Environment Variables**: Create a `.env` file in the root of your project. Here's an example:

   ```bash
   DJANGO_SECRET_KEY=your-secret-key-here
   DEBUG=True
   REDIS_URL=redis://redis:6379/1

### Using Virtual Environment

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Start Redis server (required for caching)
```bash
docker compose up -d redis
```

6. Run development server:
```bash
python manage.py runserver
```

### Using Docker

1. Build and start containers:
```bash
docker compose up --build
```

2. Create superuser:
```bash
docker compose exec web python manage.py createsuperuser
```

## API Usage

### Endpoints

- `GET /api/faqs/`
  - Retrieves all FAQs
  - Supports language filtering via query parameter

### Language Selection

```bash
# Default (English)
curl http://localhost:8000/api/faqs/

# Hindi
curl http://localhost:8000/api/faqs/?lang=hi

# Bengali
curl http://localhost:8000/api/faqs/?lang=bn
```

### Example Response

```json
[
    {
        "id": 1,
        "question": "What is this application?",
        "answer": "This is a multilingual FAQ management system",
        "created_at": "2024-03-20T10:00:00Z",
        "updated_at": "2024-03-20T10:00:00Z"
    }
]
```

## Admin Interface Usage

1. Access admin panel at `/admin/`
2. Navigate to FAQs section
3. Create new FAQ:
   - Enter question and answer in English
   - Use WYSIWYG editor for formatted answers
   - Save to trigger automatic translations

## Project Structure

```
faq-management/
├── core/                   # Project settings
├── faqs/                  # Main application
│   ├── admin.py          # Admin interface configuration
│   ├── models.py         # Data models
│   ├── serializers.py    # API serializers
│   ├── views.py          # API views
│   ├── urls.py           # URL routing
│   └── tests.py          # Unit tests
├── docker-compose.yml    # Docker configuration
├── Dockerfile           # Docker build instructions
└── requirements.txt     # Python dependencies
```

## Implementation Details

### Models
- FAQ model with question and answer fields
- FAQTranslation model for language-specific content
- Dynamic translation retrieval methods

### Caching
- Redis-based caching implementation
- Cache invalidation on content updates
- Optimized query performance

### Translation
- Automatic translation on FAQ creation
- Support for Hindi and Bengali
- Fallback to English content

### Language Extension
- **Currently Supported Languages**
  - English (en) - Primary/Default
  - Hindi (hi)
  - Bengali (bn)

- **Adding New Languages**
  - Update settings.py:
  ```python
  LANGUAGES = [
      ('en', 'English'),
      ('hi', 'Hindi'),
      ('bn', 'Bengali'),
      ('new_code', 'New Language'),  # Add new language
  ]

## Development Notes

- PEP8 compliant code
- Comprehensive unit tests
- Redis caching for performance
- Automated translation workflow

## Common Issues & Solutions

1. Translation Issues:
   - Verify googletrans==3.1.0a0 installation
   - Check internet connectivity
   - Ensure proper language codes

2. Redis Connection:
   - Verify Redis server is running
   - Check connection settings
   - Ensure proper cache configuration

