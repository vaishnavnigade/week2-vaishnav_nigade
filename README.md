## Candidate Information

- **Name:** Vaishnav Dipak Nigade
- **Email:** vniagde@deloitte.com
- **Assessment Batch:** Engineering Bootcamp(Python and React)


# Online Shopping API

A layered REST API for an online shopping application developed as part of the **Online Shopping – Application Functional API Build** case study.

The application is being developed using FastAPI, SQLAlchemy, Pydantic, and PostgreSQL. It is intended to allow users to register, log in, browse products, manage shopping carts, and place orders.

> **Current status:** The project is under development. The repository contains the primary application layers, but some integration issues and case-study alignment items still need to be completed before final submission.

---

## 1. Candidate Information

| Field | Details |
|---|---|
| Candidate Name | `<Enter your name>` |
| Candidate Email | `<Enter your email>` |
| Assessment Batch | `<Enter assessment batch>` |
| Project Name | Online Shopping API |
| Version Date | May 2026 |

---

## 2. Project Overview

ABC is expanding its physical store into an online shopping platform. This project implements the backend API for the online shopping application using Python FastAPI.

The API follows a layered architecture that separates:

- HTTP request handling
- Request and response validation
- Business rules
- Database access
- SQLAlchemy ORM models
- PostgreSQL persistence

The project is designed as a functional backend prototype rather than a production-ready e-commerce platform.

### Problem Being Solved

The physical store currently requires customers to visit the store to browse products and place orders. The application provides an online backend that supports the basic shopping lifecycle:

1. A user registers and logs in.
2. Products and categories are browsed.
3. Products are added to a shopping cart.
4. Cart quantities are updated or removed.
5. The cart is checked out.
6. An order is created and order history can be viewed.

### Key Features

The intended application features are:

- User registration
- User login and password verification
- Category management
- Product browsing
- Product search
- Shopping cart management
- Stock validation
- Cart quantity merging
- Checkout and order creation
- Order history
- Order detail retrieval
- Price capture at the time of purchase
- Layered architecture using routers, services, repositories, schemas, and models
- Automatic API documentation through FastAPI

---

## 3. Current Implementation Status

| Functional Area | Current Project Evidence | Status |
|---|---|---|
| FastAPI application | `app/main.py` | Available |
| Database configuration | `app/db/session.py` | Available |
| SQLAlchemy base class | `app/db/base.py` | Available |
| User module | User router, service, repository, schema, and model files | In progress |
| Product module | Product router, service, repository, schema, and model files | In progress |
| Category module | Category model and product-related layers | In progress |
| Cart module | Cart router, service, repository, schema, and model files | In progress |
| Order module | Order router, service, repository, schema, and model files | In progress |
| PostgreSQL connection | Configured through `DATABASE_URL` | Available if database is running |
| API documentation | FastAPI Swagger and ReDoc | Available after successful startup |
| Automated tests | No test directory visible in the current project tree | Not currently documented |
| Docker Compose | No Docker files visible in the current project tree | Not currently included |
| CI/CD pipeline | No workflow files visible in the current project tree | Not currently included |

---

## 4. Technology Stack

| Area | Technology |
|---|---|
| Programming Language | Python 3.12 |
| Web Framework | FastAPI |
| ASGI Server | Uvicorn |
| ORM | SQLAlchemy 2 |
| Schema Validation | Pydantic |
| Database | PostgreSQL |
| Configuration | `.env` file and `python-dotenv` |
| IDE | Visual Studio Code |
| API Documentation | Swagger UI and ReDoc |
| Architecture | Router, Service, Repository, Schema, and Model layers |

SQLite may be used for local experimentation only if the database configuration and SQLAlchemy connection settings are changed accordingly. The current configuration is designed for PostgreSQL.

---

## 5. Application Architecture

The application follows a layered architecture.

### Request Flow

The request flow is:

1. The client sends an HTTP request.
2. FastAPI matches the request with a router endpoint.
3. Pydantic validates the request body and parameters.
4. The router obtains a database session using `get_db`.
5. The router calls the relevant service.
6. The service applies business rules and validations.
7. The repository performs database operations.
8. SQLAlchemy maps database records to model objects.
9. The service returns the result to the router.
10. FastAPI serializes the response using a Pydantic response schema.

### Layer Responsibilities

#### Router Layer

The router layer contains:

- API paths
- HTTP methods
- Request and response schemas
- Dependency injection
- HTTP status codes
- Basic exception-to-response mapping

The current router modules are located in `app/routers/`.

#### Service Layer

The service layer contains:

- Business logic
- Validation rules
- Coordination between repositories
- Cart quantity calculations
- Stock checks
- Checkout logic
- User registration and login logic

The current service modules are located in `app/services/`.

#### Repository Layer

The repository layer contains:

- Database queries
- Record retrieval
- Record creation
- Update operations
- Delete operations
- Commit and refresh operations

The current repository modules are located in `app/repositories/`.

#### Model Layer

The model layer contains SQLAlchemy ORM classes that represent database tables and relationships.

The current model modules are located in `app/models/`.

#### Schema Layer

The schema layer contains Pydantic models for:

- Request validation
- Response serialization
- Public response fields
- Password input handling
- Product, cart, and order payloads

The current schema modules are located in `app/schemas/`.

---

## 6. Project Structure

The current project structure is organized as follows:

    .
    ├── app
    │   ├── db
    │   │   ├── base.py
    │   │   └── session.py
    │   │
    │   ├── models
    │   │   ├── user.py
    │   │   ├── category.py
    │   │   ├── product.py
    │   │   ├── cart.py
    │   │   └── order.py
    │   │
    │   ├── repositories
    │   │   ├── user_repository.py
    │   │   ├── product_repository.py
    │   │   ├── cart_repository.py
    │   │   └── order_repository.py
    │   │
    │   ├── routers
    │   │   ├── user_router.py
    │   │   ├── product_router.py
    │   │   ├── cart_router.py
    │   │   └── order_router.py
    │   │
    │   ├── schemas
    │   │   ├── user_schema.py
    │   │   ├── product_schema.py
    │   │   ├── cart_schema.py
    │   │   └── order_schema.py
    │   │
    │   ├── services
    │   │   ├── user_service.py
    │   │   ├── product_service.py
    │   │   ├── cart_service.py
    │   │   └── order_service.py
    │   │
    │   ├── utils
    │   │   ├── exceptions.py
    │   │   └── helpers.py
    │   │
    │   ├── __init__.py
    │   └── main.py
    │
    ├── .env
    ├── .gitignore
    ├── requirements.txt
    └── venv

The `venv` directory is a local Python virtual environment and should not be committed to Git. The `.env` file should also remain excluded because it may contain database credentials.

---

## 7. Database Design

The current SQLAlchemy models represent the following entities.

### Users

| Field | Purpose |
|---|---|
| `id` | Primary key |
| `email` | Unique user email |
| `hashed_password` | Hashed password value |

The case study also mentions user name and mobile number. These fields should be added to the model and schemas if they are required for the final assessment submission.

### Categories

| Field | Purpose |
|---|---|
| `id` | Primary key |
| `name` | Unique category name |
| `description` | Optional category description |

A category can contain multiple products.

### Products

| Field | Purpose |
|---|---|
| `id` | Primary key |
| `name` | Product name |
| `description` | Product description |
| `price` | Product price |
| `stock` | Available product quantity |
| `category_id` | Foreign key to the category |
| `created_at` | Product creation timestamp |

The case study calls the stock field `AvailableQuantity`. The current implementation uses `stock`, which is acceptable if the name is used consistently throughout the model, schemas, services, and API documentation.

The case study also mentions `ProductUrl`. This field should be added if product image or product URL support is required.

### Cart Items

| Field | Purpose |
|---|---|
| `id` | Primary key |
| `user_id` | Foreign key to the user |
| `product_id` | Foreign key to the product |
| `quantity` | Number of units in the cart |
| `added_at` | Time the item was added |

A unique constraint on `user_id` and `product_id` prevents duplicate cart lines for the same user and product.

### Orders

| Field | Purpose |
|---|---|
| `id` | Primary key |
| `user_id` | Foreign key to the user |
| `status` | Current order status |
| `total_amount` | Total order amount |
| `created_at` | Order creation timestamp |

The case study includes `PaymentMethod`. The current visible order model does not show this field, so it should be added if payment method is part of the required checkout functionality.

### Order Items

| Field | Purpose |
|---|---|
| `id` | Primary key |
| `order_id` | Foreign key to the order |
| `product_id` | Foreign key to the product |
| `quantity` | Quantity purchased |
| `unit_price` | Product price at checkout |

The case study refers to this table as `OrderDetails`. The current implementation uses the name `OrderItem`. This is acceptable as an internal naming decision if the relationship and API behavior match the case-study requirement.

The `unit_price` field stores the purchase-time price so that later product price changes do not alter historical orders.

---

## 8. Entity Relationships

The intended relationships are:

- One user can have many cart items.
- One user can place many orders.
- One category can contain many products.
- One product can appear in many cart items.
- One order can contain many order items.
- One product can appear in many order items.
- A user-product pair should have at most one active cart line.

Before creating tables, all model modules must be imported so that every table is registered in `Base.metadata`. In particular, the order and order-item models must also be imported before `create_all` is called.

---

## 9. API Functional Areas

The API is organized into the following functional areas.

### User APIs

The user module is intended to support:

- User registration
- Duplicate email validation
- Password hashing
- Login using email and password
- Invalid credential handling
- Public user responses without exposing the password hash

### Product and Category APIs

The catalog module is intended to support:

- Category creation
- Category retrieval
- Product creation
- Product retrieval
- Product listing
- Product search by name
- Product filtering by category
- Product existence validation
- Product stock display

### Cart APIs

The cart module is intended to support:

- View a user's cart
- Add a product to the cart
- Increase the quantity of an existing cart item
- Update cart quantity
- Remove a cart item
- Validate that the user exists
- Validate that the product exists
- Validate available stock
- Calculate a cart summary

### Order APIs

The order module is intended to support:

- Checkout
- Empty-cart validation
- Stock validation during checkout
- Order total calculation
- Price capture at checkout
- Stock reduction
- Cart clearing after successful checkout
- Order history
- Order detail retrieval

The exact route prefixes and paths should be confirmed from the decorators in the router files and from the generated OpenAPI documentation.

---

## 10. Validation Rules

The following validation rules are required or expected for the case study.

### User Validation

- Name must not be empty if included in the user model.
- Email must have a valid format.
- Email must be unique.
- Password must satisfy the minimum length requirement.
- Passwords must not be stored in plain text.
- Mobile must be numeric and have an appropriate length if included.

### Product and Category Validation

- Category names should be unique.
- Product names should be unique if required by the case study.
- Product price must be greater than zero.
- Product stock must not be negative.
- A product must reference an existing category.
- A product must exist before it can be added to a cart.

### Cart Validation

- Cart quantity must be greater than zero.
- A user must exist before accessing the cart.
- A product must exist before adding it to the cart.
- The requested quantity must not exceed available stock.
- If a product is already in the cart, the new quantity should be combined with the existing quantity.
- The combined quantity must also be checked against available stock.
- A cart item must exist before it can be updated or removed.

### Order Validation

- A user must exist before checkout.
- The user must have at least one cart item.
- Ordered quantity must not exceed available stock.
- Payment method must be valid if payment method is implemented.
- Order total must be calculated by the service layer.
- Product prices should be copied into order items during checkout.
- Stock should be reduced only after the order can be created successfully.
- The cart should be cleared after successful checkout.

---

## 11. Setup Instructions

### Prerequisites

Install the following before running the project:

- Python 3.12
- PostgreSQL
- Visual Studio Code or another Python IDE
- Git
- `pip`

### Create a Virtual Environment

On Windows PowerShell:

    py -3.12 -m venv venv
    .\venv\Scripts\Activate.ps1

On macOS or Linux:

    python3 -m venv venv
    source venv/bin/activate

### Install Dependencies

From the project root:

    python -m pip install --upgrade pip
    pip install -r requirements.txt

The requirements file should include the packages required by the application, including FastAPI, Uvicorn, SQLAlchemy, Pydantic, database configuration support, and the PostgreSQL driver.

### Configure the Database

Create a PostgreSQL database for the application, for example:

    online_shopping

Create a `.env` file in the project root and add the database connection string:

    DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/online_shopping

Update the username, password, host, port, and database name to match the local PostgreSQL installation.

Do not commit `.env` to Git.

### Start the Application

From the project root, run:

    uvicorn app.main:app --reload

The API should start on the default local development port.

### Open API Documentation

After the application starts, use the following paths:

- `/docs` for Swagger UI
- `/redoc` for ReDoc
- `/openapi.json` for the generated OpenAPI specification

### Database Table Initialization

The current application uses SQLAlchemy table creation during application startup.

This approach can create missing tables for a prototype, but it does not provide versioned database migrations. Alembic should be considered for future schema changes.

---

## 12. Suggested Functional Test Flow

Use Swagger UI to test the following sequence:

1. Open the user registration endpoint.
2. Register a new user.
3. Log in using the registered email and password.
4. Create or retrieve a product category.
5. Create a product associated with the category.
6. Retrieve the product list.
7. Search for the product.
8. Add the product to the user's cart.
9. Retrieve the cart.
10. Update or remove the cart item.
11. Add an item again with a valid quantity.
12. Checkout the cart.
13. Retrieve the created order.
14. Retrieve the user's order history.
15. Confirm that product stock was reduced.
16. Confirm that the cart was cleared.

---

## 13. Current Issues to Resolve

### Repository Method Mismatch

The current runtime error is:

    AttributeError: module 'app.repositories.user_repository' has no attribute 'get_user'

The cart service calls `user_repository.get_user(db, user_id)`, but the visible user repository currently contains `get_user_by_email` and `create_user`.

The service and repository must use the same method name and purpose. The cart service requires a user lookup by ID, so the repository needs a corresponding user-by-ID operation or the service must call an existing method with the correct behavior.

### Router Registration

The application entry point must include all required routers:

- User router
- Product router
- Cart router
- Order router

The earlier `main.py` version showed only the user router being included. Confirm that all current routers are registered before testing the complete application.

### Model Registration

Every SQLAlchemy model must be imported before `Base.metadata.create_all(bind=engine)` runs.

Verify that the following models are registered:

- `User`
- `Category`
- `Product`
- `CartItem`
- `Order`
- `OrderItem`

### Case-Study Field Alignment

The following fields from the case study should be reviewed against the current models:

- User name
- User mobile
- Product URL
- Payment method
- Product name uniqueness
- Available product quantity
- Order detail naming

If any of these fields are required for assessment evaluation, add them consistently to the model, schema, repository, service, router, and database configuration.

---

## 14. Assumptions

The following assumptions are made for this prototype:

- Authentication is currently based on email and password.
- Login verification does not necessarily issue a JWT or session token.
- Cart and order endpoints may currently receive a `user_id` directly.
- Administrator authorization is not implemented.
- Product and category creation are available for development or testing.
- Passwords are intended to be stored as hashes rather than plain text.
- PostgreSQL is the primary database.
- SQLAlchemy automatically creates missing tables during application startup.
- Product prices are captured in order items during checkout.
- Payment processing is not connected to an external payment provider.
- The application is intended for functional assessment and learning purposes.

---

## 15. Known Limitations

The current project has the following limitations:

- A user repository method mismatch currently prevents cart processing.
- Authentication ownership is not fully enforced if endpoints accept `user_id` directly.
- JWT or session-based authentication is not currently confirmed.
- Administrator authorization is not currently confirmed.
- Database migrations are not included.
- Automated tests are not visible in the current project structure.
- Docker and Docker Compose files are not visible in the current project structure.
- CI/CD workflow files are not visible in the current project structure.
- Pagination is not currently confirmed.
- Advanced logging and monitoring are not currently included.
- Payment processing is not implemented.
- Password reset and email verification are not implemented.
- Concurrent checkout protection should be strengthened before production use.
- Database integrity errors should be translated into clear API responses.
- Exact endpoint prefixes should be verified from the router implementations.

---

## 16. Development Milestones

### Milestone 1: Project Setup

- Create the FastAPI application.
- Create the project folders.
- Configure the database engine and session.
- Create the SQLAlchemy base class.
- Create the initial database models.

### Milestone 2: User and Catalog APIs

- Implement user registration.
- Implement login and password verification.
- Implement category operations.
- Implement product creation and retrieval.
- Implement product search and filtering.

### Milestone 3: Cart APIs

- Implement cart retrieval.
- Implement add-to-cart functionality.
- Merge duplicate product lines.
- Validate product stock.
- Implement update and remove operations.
- Implement cart summary.

### Milestone 4: Order APIs

- Implement checkout.
- Validate that the cart is not empty.
- Calculate the order total.
- Capture product prices.
- Reduce product stock.
- Clear the cart after successful checkout.
- Implement order history and order details.

### Milestone 5: Exception Handling

- Add not-found errors.
- Add duplicate-record handling.
- Add invalid-quantity handling.
- Add out-of-stock handling.
- Add invalid-login handling.
- Map service errors to appropriate HTTP responses.

### Milestone 6: Final Verification

- Confirm that all routers are registered.
- Confirm that all models are imported.
- Resolve repository method mismatches.
- Verify all case-study fields.
- Test the complete user-to-checkout workflow.
- Confirm that secrets and virtual environments are excluded from Git.

---

## 17. Submission Checklist

- [ ] Candidate information has been completed.
- [ ] The application starts successfully with Uvicorn.
- [ ] The database connection is configured through `.env`.
- [ ] `.env` is excluded from Git.
- [ ] `venv` is excluded from Git.
- [ ] All required dependencies are present in `requirements.txt`.
- [ ] All SQLAlchemy models are imported before table creation.
- [ ] All required routers are registered in `main.py`.
- [ ] The `get_user` repository/service mismatch is resolved.
- [ ] User registration works.
- [ ] User login works.
- [ ] Product listing works.
- [ ] Product search works.
- [ ] Cart add, update, and remove operations work.
- [ ] Stock validation works during cart operations.
- [ ] Checkout works with a non-empty cart.
- [ ] Order total is calculated correctly.
- [ ] Product stock is reduced after checkout.
- [ ] The cart is cleared after checkout.
- [ ] Order history works.
- [ ] Order details work.
- [ ] Swagger documentation displays the expected endpoints.
- [ ] Case-study fields have been reviewed and implemented where required.
- [ ] No passwords or database credentials are committed.
- [ ] README accurately reflects the implemented functionality.

---

## 18. Conclusion

This project provides the foundation for a layered FastAPI-based online shopping backend. It demonstrates FastAPI routing, Pydantic validation, SQLAlchemy models, repository-based database access, service-layer business rules, cart management, stock validation, and checkout processing.

Before final submission, the priority actions are:

1. Resolve the missing `get_user` repository method.
2. Register every required router in `main.py`.
3. Import every model before database table creation.
4. Compare the current models with the case-study fields.
5. Test the complete registration-to-checkout workflow.
6. Update this README if the implementation changes.
