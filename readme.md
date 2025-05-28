# Location Microservice

A Django REST API microservice for managing and retrieving location data (countries, states, and cities).

## Features

- Public API endpoints (no authentication required)
- Search countries, states, and cities by name
- Filter locations hierarchically (by country, state)
- Global search across all location entities
- Pagination support
- Swagger API documentation

## Installation and Setup

### Prerequisites

- Python 3.8+
- PostgreSQL

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
DEBUG=True
SECRET_KEY=your_secret_key
DB_NAME=locations_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Installation

1. Clone the repository
2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Start the server:

```bash
python manage.py runserver
```

## Docker Deployment

Build and run the Docker container:

```bash
docker build -t location-service .
docker run -p 8000:8000 --env-file .env location-service
```

## API Endpoints

### Base URL

```
http://localhost:8000/api/v1/
```

### Swagger Documentation

```
http://localhost:8000/swagger/
```

### Countries

- `GET /api/v1/countries/` - List all countries with pagination
- `GET /api/v1/countries/{id}/` - Get country details with states
- `GET /api/v1/countries/{id}/full_details/` - Get country with all states and cities
- `GET /api/v1/countries/search/?name={name}` - Search countries by name

### States

- `GET /api/v1/states/` - List all states with pagination
- `GET /api/v1/states/{id}/` - Get state details with cities
- `GET /api/v1/states/by_country/?country_id={id}` - Get states by country ID
- `GET /api/v1/states/search/?name={name}&country_id={country_id}` - Search states by name with optional country filter

### Cities

- `GET /api/v1/cities/` - List all cities with pagination
- `GET /api/v1/cities/{id}/` - Get city details
- `GET /api/v1/cities/by_state/?state_id={id}&country_id={country_id}` - Get cities by state ID
- `GET /api/v1/cities/by_country/?country_id={id}` - Get cities by country ID
- `GET /api/v1/cities/search/?name={name}&state_id={state_id}&country_id={country_id}` - Search cities by name with optional state and country filters

### Global Search

- `GET /api/v1/search/?q={query}` - Search across countries, states, and cities

## Development

### Running Tests

```bash
python manage.py test
```