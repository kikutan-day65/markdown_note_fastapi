# markdown_note_fastapi

[日本語版 README](./README_JA.md)

> This project is currently under development, and its specifications and features may be changed or expanded in the future.

This project is a Markdown article management Web API developed with FastAPI.

It implements features such as user authentication, articles, tags, comments, and likes.
To improve maintainability, responsibilities are separated into Router, Service, and Repository layers.

## Main Features

- User registration and authentication
- Retrieval, update, and deletion of user profiles
- Creation, retrieval, update, and deletion of Markdown articles
- Retrieval of tags
- Creation, retrieval, update, and deletion of comments
- Liking and unliking articles
- Pagination for article and comment lists
- Ownership-based authorization for updating and deleting articles and comments
- Soft deletion using `deleted_at`

## Design Approach

The application is mainly organized into the following layers to separate responsibilities.

- **Router**
  - Receives HTTP requests
  - Defines request parameters and responses
  - Calls the Service layer

- **Service**
  - Handles application use cases and business logic
  - Performs authorization checks
  - Coordinates operations involving multiple repositories

- **Repository**
  - Handles database operations using SQLAlchemy
  - Retrieves, creates, updates, and deletes data

By separating the API layer, business logic, and data access logic, this project aims to improve code readability, maintainability, and testability.

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT Authentication

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kikutan-day65/markdown_note_fastapi.git
cd markdown_note_fastapi
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory and configure the database connection and authentication settings.

```env
DATABASE_URL=postgresql+psycopg://<username>:<password>@localhost:5432/<database>
SECRET_KEY=<your-secret-key>
```

Modify the environment variable names and values according to the actual project configuration.

### 5. Run Database Migrations

```bash
alembic upgrade head
```

### 6. Start the FastAPI Application

```bash
uvicorn app.main:app --reload
```

### 7. View the API Documentation

After starting the application, Swagger UI is available at:

```text
http://127.0.0.1:8000/docs
```

ReDoc is available at:

```text
http://127.0.0.1:8000/redoc
```

## Future Plans

- Improve refresh token handling
- Add test code
- Improve error handling
- Expand the README and API documentation
- Integrate with a frontend developed using React and TypeScript
- Set up a deployment environment
