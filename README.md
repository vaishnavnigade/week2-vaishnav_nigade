# Online Shopping API

A layered REST API for a small online shopping system. It is built with FastAPI,
Pydantic, SQLAlchemy 2, and PostgreSQL, and supports user registration/login,
catalog management, shopping carts, and cart checkout.

FastAPI generates interactive API documentation automatically:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Features

- Register a user and verify password-based login.
- Hash passwords using `pwdlib`'s recommended password hasher.
- Create product categories and products.
- List products and retrieve product/category details.
- Add products to a user's cart, merge duplicate cart lines, and remove lines.
- Validate stock before adding items and again during checkout.
- Convert a cart into an order, capture the price at purchase time, reduce stock,
  and clear the cart.
- Persist data in PostgreSQL through SQLAlchemy ORM models.
- Run locally or as a Docker Compose stack with PostgreSQL.

## Architecture

The application uses a layered architecture. HTTP-specific concerns stay in the
router layer, business rules live in services, and database access is isolated in
repositories.

```mermaid
flowchart LR
    Client["API client"] --> FastAPI["FastAPI application"]
    FastAPI --> Routers["Router layer"]
    Routers --> Schemas["Pydantic schemas"]
    Routers --> Services["Service layer"]
    Services --> Repositories["Repository layer"]
    Services --> Models["SQLAlchemy models"]
    Repositories --> Models
    Repositories --> Session["SQLAlchemy session"]
    Session --> PostgreSQL[(PostgreSQL)]
    Services --> Utilities["Helpers and domain exceptions"]
```

### Request lifecycle

1. A client sends an HTTP request to a FastAPI route.
2. FastAPI validates path parameters and the JSON body using a Pydantic schema.
3. The `get_db` dependency creates one SQLAlchemy session for the request.
4. The router calls a service and translates known domain exceptions into HTTP
   status codes.
5. The service enforces business rules and coordinates one or more repositories.
6. Repositories execute ORM queries and persist changes in PostgreSQL.
7. FastAPI serializes the returned ORM object through the declared response schema.
8. The database session is closed after the response completes.

### Layer-by-layer guide

#### Application entry point — `app/main.py`

- Creates the `FastAPI` application.
- Imports `Base` and calls `Base.metadata.create_all(bind=engine)` during startup
  import. This creates missing tables; it does not perform versioned migrations.
- Registers the authentication, product, cart, and order routers.
- Exposes `GET /` as a simple health/status endpoint.

#### Router layer — `app/routers/`

Routers define URLs, HTTP methods, request/response schemas, dependency injection,
and HTTP status codes. They contain very little business logic.

- `user_router.py`: registration and login endpoints under `/auth`.
- `product_router.py`: category and product endpoints under `/products`.
- `cart_router.py`: cart endpoints under `/carts`.
- `order_router.py`: checkout and order queries under `/orders`.

The routers convert domain exceptions such as `NotFoundError` and
`OutOfStockError` into `404`, `400`, or `401` responses.

#### Schema layer — `app/schemas/`

Pydantic models form the API contract and keep request validation separate from
database models.

- `user_schema.py`: registration, login, and public user response shapes.
- `product_schema.py`: category/product creation and read shapes.
- `cart_schema.py`: positive cart quantities and nested product responses.
- `order_schema.py`: order-line and order response shapes using `Decimal` prices.

Read schemas enable `from_attributes`, allowing Pydantic to serialize SQLAlchemy
objects without exposing internal fields such as `hashed_password`.

#### Service layer — `app/services/`

Services implement use cases and business rules:

- `user_service.py` rejects duplicate emails, hashes new passwords, and validates
  login credentials without revealing whether the email or password was wrong.
- `product_service.py` requires a category to exist before creating a product and
  raises a domain-level not-found error for missing records.
- `cart_service.py` verifies the user and product, checks the combined cart
  quantity against available stock, and increases an existing line instead of
  creating duplicate user/product rows.
- `order_service.py` checks the user and cart, rechecks stock, snapshots each
  product's price, calculates the total, decrements stock, creates the order, and
  empties the cart.

#### Repository layer — `app/repositories/`

Repositories are the persistence boundary. They accept a SQLAlchemy `Session`,
run queries, and commit/refresh ORM objects. `selectinload` is used where nested
product or order data is needed after a query.

- `user_repository.py`: users by ID/email and user creation.
- `product_repository.py`: category/product creation and lookup, product listing,
  and stock updates.
- `cart_repository.py`: cart lookup, listing, quantity updates, and deletion.
- `order_repository.py`: order creation, eager-loaded lookup, listing, and status
  updates.

#### Model layer — `app/models/`

SQLAlchemy declarative models define the relational data model:

```mermaid
erDiagram
    USERS ||--o{ CART_ITEMS : has
    USERS ||--o{ ORDERS : places
    CATEGORIES ||--o{ PRODUCTS : contains
    PRODUCTS ||--o{ CART_ITEMS : appears_in
    ORDERS ||--|{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : purchased_as

    USERS {
        int id PK
        string email UK
        string hashed_password
    }
    CATEGORIES {
        int id PK
        string name UK
        string description
    }
    PRODUCTS {
        int id PK
        string name
        text description
        decimal price
        int stock
        int category_id FK
        datetime created_at
    }
    CART_ITEMS {
        int id PK
        int user_id FK
        int product_id FK
        int quantity
        datetime added_at
    }
    ORDERS {
        int id PK
        int user_id FK
        string status
        decimal total_amount
        datetime created_at
    }
    ORDER_ITEMS {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
    }
```

Important constraints and modeling decisions:

- User emails and category names are unique.
- `(user_id, product_id)` is unique in `cart_items`, so one product has at most
  one line per user's cart.
- Money is stored as `NUMERIC(10, 2)` and represented by `Decimal` in API schemas.
- `OrderItem.unit_price` preserves the purchase-time price even if the product's
  current price later changes.
- Deleting an order through the ORM also deletes its order items because the
  relationship uses `delete-orphan` cascading.

#### Database layer — `app/db/`

- `base.py` defines the shared SQLAlchemy `DeclarativeBase`.
- `models/__init__.py` imports every ORM model, and `main.py` loads that module
  before table creation so all tables are registered in `Base.metadata` without
  circular imports.
- `session.py` loads `.env`, validates `DATABASE_URL`, creates the connection pool
  and session factory, and exposes the per-request `get_db` dependency.
- `pool_pre_ping=True` checks pooled connections before use and avoids returning a
  stale connection to a request.

#### Utilities — `app/utils/`

- `helpers.py` hashes and verifies passwords.
- `exceptions.py` defines framework-independent errors used by services and mapped
  to HTTP responses by routers.

## Project structure

```text
.
├── app
│   ├── db              # Engine, session factory, and declarative base
│   ├── models          # SQLAlchemy database entities and relationships
│   ├── repositories    # Database queries and persistence operations
│   ├── routers         # FastAPI endpoints and HTTP error mapping
│   ├── schemas         # Pydantic request/response contracts
│   ├── services        # Business rules and use-case orchestration
│   ├── utils           # Password helpers and domain exceptions
│   └── main.py         # App creation, table initialization, router registration
├── tests               # Pytest API integration and business-rule tests
├── .github/workflows   # GitHub Actions CI workflow
├── .dockerignore
├── .env.example
├── compose.yaml        # API + PostgreSQL development stack
├── Dockerfile          # API container image
├── requirements-dev.txt
└── requirements.txt
```

## API endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/` | Application health/status response |
| `POST` | `/auth/register` | Register a user |
| `POST` | `/auth/login` | Verify user credentials |
| `POST` | `/products/categories` | Create a category |
| `GET` | `/products/categories/{category_id}` | Get a category and its products |
| `POST` | `/products` | Create a product in an existing category |
| `GET` | `/products` | List all products |
| `GET` | `/products/{product_id}` | Get a product |
| `POST` | `/carts/{user_id}/items` | Add/increment a cart item |
| `GET` | `/carts/{user_id}/items` | List a user's cart items |
| `DELETE` | `/carts/items/{cart_item_id}` | Remove a cart item |
| `POST` | `/orders/{user_id}/checkout` | Turn the user's cart into an order |
| `GET` | `/orders/{order_id}` | Get an order and its items |
| `GET` | `/orders/users/{user_id}` | List a user's orders |

## Configuration

The application requires `DATABASE_URL` in the environment or a root `.env` file.
Copy the supplied template before local development:

```bash
cp .env.example .env
```

The default local value is:

```dotenv
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/online_shopping
```

Do not commit `.env`. It is ignored because it may contain database credentials.

## Run with Docker Compose (recommended)

Prerequisites: Docker Engine/Desktop with Docker Compose v2.

1. Optionally create `.env` to override the non-secret development defaults:

   ```bash
   cp .env.example .env
   ```

2. Build the API image and start both services:

   ```bash
   docker compose up --build
   ```

3. Open `http://localhost:8000/docs` or verify the API:

   ```bash
   curl http://localhost:8000/
   ```

Compose waits for PostgreSQL's health check before starting the API. The API uses
the internal hostname `db`, while PostgreSQL is also published on host port `5432`
for database tools. Data is retained in the named `postgres_data` volume.

Useful commands:

```bash
# Start in the background
docker compose up --build -d

# Follow API logs
docker compose logs -f api

# Stop the stack but retain database data
docker compose down

# Stop and delete the PostgreSQL volume (all application data is lost)
docker compose down -v
```

If ports `8000` or `5432` are already occupied, change `API_PORT` or
`POSTGRES_PORT` in `.env` before starting Compose.

## Run locally

Prerequisites:

- Python 3.10 or newer (Python 3.12 is used by the Docker image).
- A running PostgreSQL server and an existing database.

Create the default database with your PostgreSQL tooling, then run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Adjust `DATABASE_URL` in `.env` if the PostgreSQL username, password, host, port,
or database name differs. When the application starts, SQLAlchemy creates missing
tables automatically.

## Example workflow

With the server running, these requests exercise the main checkout path:

```bash
# Register a user (the first user normally receives ID 1)
curl -X POST http://localhost:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"shopper@example.com","password":"change-me"}'

# Create a category
curl -X POST http://localhost:8000/products/categories \
  -H 'Content-Type: application/json' \
  -d '{"name":"Books","description":"Printed books"}'

# Create a product in category 1
curl -X POST http://localhost:8000/products \
  -H 'Content-Type: application/json' \
  -d '{"name":"FastAPI Guide","price":"29.99","stock":10,"category_id":1}'

# Add product 1 to user 1's cart
curl -X POST http://localhost:8000/carts/1/items \
  -H 'Content-Type: application/json' \
  -d '{"product_id":1,"quantity":2}'

# Checkout the cart
curl -X POST http://localhost:8000/orders/1/checkout
```

## Testing

Install the development dependencies and run the test suite:

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

Local tests use `/tmp/online-shopping-api-test.db` by default and reset its schema
before every test. To test against PostgreSQL, export a URL whose database name
contains `test`:

```bash
export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/online_shopping_test
python -m pytest -q
```

The safety guard refuses to run the destructive test fixture against a PostgreSQL
database whose name does not contain `test`.

The tests cover health/OpenAPI responses, authentication success and errors,
catalog creation, cart merging and deletion, accumulated stock validation,
checkout, order retrieval, inventory updates, and missing-record responses.

## GitHub Actions CI/CD pipeline

The workflow at `.github/workflows/ci.yml` runs for every push, pull request, and
manual dispatch. It performs two jobs:

1. Starts an isolated PostgreSQL 16 service, installs dependencies, validates the
   environment and Compose file, compiles the Python sources, and runs Pytest.
2. Builds the production Dockerfile after the test job passes.

The workflow validates that the application is ready for delivery but does not
publish or deploy the image. Add a registry/login and deployment job after
choosing a deployment target and configuring its GitHub secrets.

## Current scope and production considerations

This project is an educational API rather than a production-ready shop:

- Login verifies credentials but does not issue a session or JWT. Cart/order
  endpoints accept `user_id` directly and therefore do not enforce ownership.
- Category and product writes have no administrator authorization.
- Tables are created with `create_all`; use Alembic migrations for controlled
  schema evolution.
- Repository methods commit individually. Checkout should use one explicit
  database transaction with row locking or another concurrency strategy before
  handling real inventory.
- Duplicate category names and other database integrity errors are not translated
  into tailored HTTP responses.
- Pagination, structured logging, rate limits, and monitoring are not included yet.
- The defaults in `.env.example` and `compose.yaml` are for local development;
  replace them with secret-managed credentials in deployed environments.
