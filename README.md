# Django Learning Journey

Building backend skills step-by-step using Django.

---

## Core Backend

- Django project structure
- Apps architecture
- URL routing
- Views vs ViewSets
- Serializers (validation, transformation)
- Django ORM (CRUD, relations)

---

## REST API (DRF)

- ModelViewSet
- APIView
- Routers
- Custom actions (@action)
- Soft delete pattern

---

## Authentication and Security

- JWT authentication (SimpleJWT)
- Login / Register APIs
- Access and Refresh tokens
- Protected routes
- Bearer token flow
- Production auth lifecycle understanding

---

## Permissions (Access Control)

- IsAuthenticated
- IsAdminUser
- Custom permission classes
- Owner-based access (IsOwner)
- Action-based permissions (get_permissions)
- Role-based security design

---

## Database and ORM (Advanced)

- Query optimization
- select_related
- prefetch_related
- Indexing
- Performance mindset
- ORM vs raw SQL understanding

---

## Filtering / Search / Ordering

- Manual filtering
- django-filter (FilterSet)
- SearchFilter
- OrderingFilter
- Query parameter based APIs

---

## Pagination

- PageNumberPagination
- LimitOffsetPagination
- CursorPagination

---

## Caching (Performance)

- Django cache framework
- Redis cache backend
- View caching
- Manual cache logic
- Cache invalidation basics
- Per-user cache keys
- API speed optimization

---

## Background Tasks (Async)

- Celery setup
- Redis broker
- Task queues
- Non-blocking operations (emails, heavy work)

---

## DevOps / Production Setup

- Docker
- Dockerfile
- docker-compose
- Postgres container
- Redis container
- Celery worker container
- Volume persistence
- Environment variables
- Full local production-like stack

---

## Logging and Debugging

- Django logging config
- INFO / WARNING / ERROR logs
- Structured logs
- Debugging requests
- Monitoring mindset

---

## Real-world Patterns Implemented

- Soft delete
- Ownership control
- Background email sending
- API caching
- Pagination and filtering combined
- Secure endpoints
- Production database
- Containerized services
