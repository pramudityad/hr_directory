# HR Directory Microservice

This is a Flask-based microservice for an HR directory that provides an API to search for employees within organizations. It utilizes SQLAlchemy for ORM and Flask-Limiter for rate limiting.

## Features

- **Employee Search**: Search for employees by their first or last name.
- **Pagination**: Supports pagination for search results.
- **Rate Limiting**: Limits API requests to prevent abuse.
- **Configurable Columns**: Organizations can configure which employee details are returned in the response.

## Technologies Used

- **Python**: Programming language.
- **Flask**: Micro web framework for Python.
- **Flask-SQLAlchemy**: ORM for database interactions.
- **Flask-Limiter**: Rate limiting for Flask routes.
- **SQLite**: Lightweight database for storage.


## Installation

1. Clone the repository
2. Create and activate a virtual environment
3. Install the required packages `pip install -r requirements.txt`
4. populate the data `python populate.py`
5. run the app `python app.py`

## API Endpoints

### Search Employees

- **Endpoint**: `/employees/search`
- **Method**: `GET`

#### Query Parameters:
- `org_id` (required): The ID of the organization.
- `query` (optional): Search term for first or last name.
- `page` (optional): Page number for pagination (default is 1).
- `per_page` (optional): Number of results per page (default is 10).

#### Response:
- `200 OK`: Successful search with employee data.
- `400 Bad Request`: If `org_id` is missing.
- `404 Not Found`: If the organization ID does not exist.
- `429 Too Many Requests`: If the request limit is exceeded.

#### Example Request
```
curl --request GET \
  --url 'http://127.0.0.1:5000/employees/search?query=John&org_id=1&page=1&per_page=10'
```

#### Example Response
```
{
   "page": 1,
   "results": [
      {
         "department": "Engineering",
         "email": "john.doe@example.com",
         "first_name": "John",
         "last_name": "Doe"
      }
   ],
   "total_pages": 1,
   "total_results": 1
}
```

## Testing

1. Ensure you have the required packages installed.
2. Run `python -m unittest test_app.py`