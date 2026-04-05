# Finance Dashboard Backend API

A backend system built using **FastAPI** and **SQLModel** to manage financial records with role-based access control and dashboard analytics.

---

## Project Overview

This project simulates a backend for a finance dashboard where multiple users interact with financial records based on their roles.

The system supports:

* User management with roles (Admin, Analyst, Viewer)
* Financial record management (income & expenses)
* Dashboard analytics (totals, category breakdown, recent activity)
* Role-based access control (RBAC)
* Pagination and filtering for efficient data handling

---

## 🛠️ Tech Stack

* **Framework:** FastAPI
* **Database:** SQLite
* **ORM:** SQLModel
* **Validation:** Pydantic
* **Authentication (Mock):** Header-based (`X-User-Id`)
* **API Docs:** Swagger UI (`/docs`)

---

## 📂 Project Structure

```
finance_backend/
│
├── database.py        # Database engine & session
├── models.py          # SQLModel database models
├── schemas.py         # Pydantic schemas (DTOs)
├── dependencies.py    # RBAC and authentication logic
├       
├── main.py            # App entry point
│
├── routers/
│   ├── users.py       # User APIs
│   ├── records.py     # Financial record APIs
│   └── dashboard.py   # Dashboard analytics APIs
│
└── database.db         # SQLite database file
```

---

## Setup Instructions

### Clone the repository

```bash
git clone <your-repo-url>
cd finance_backend
```

### Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### run the server

```bash
uvicorn main:app --reload
```

---

## 📘 API Documentation

Once the server is running, open:

http://127.0.0.1:8000/docs

You can:

* Test APIs directly
* Send requests
* View schemas

---

## 👤 User Roles & Access Control

| Role    | Permissions                          |
| ------- | ------------------------------------ |
| Admin   | Full access (create, update, delete) |
| Analyst | View records & dashboard             |
| Viewer  | Restricted access                    |

### Authentication Approach

This project uses **mock authentication** via request headers:

```
X-User-Id: <user_id>
```

This simplifies testing while demonstrating RBAC logic.

---

## Features Implemented

### 1️⃣ User Management

* Create users
* Assign roles (Admin / Analyst / Viewer)
* Manage user status

---

### 2️⃣ Financial Records

* Create, view, update, delete records
* Fields include:

  * Amount (Decimal for precision)
  * Type (income/expense)
  * Category
  * Date
  * Notes

---

### 3️⃣ Dashboard APIs

Efficient database-level aggregations:

* Total Income
* Total Expenses
* Net Balance
* Category-wise totals
* Recent activity (last 5 records)

Implemented using SQL aggregation (`SUM`, `GROUP BY`, `ORDER BY`)

---

### Role-Based Access Control (RBAC)

Implemented using FastAPI dependencies:

* Admin-only operations
* Analyst/Admin read access
* Viewer restrictions

---

### Pagination & Filtering

Efficient data retrieval:

```
GET /records/?skip=0&limit=10
GET /records/?type=income
GET /records/?category=food
```

---

### Soft Delete

Instead of permanently deleting records:

```
is_deleted = True
```

Ensures:

* Data safety
* Audit capability

---

## Key Design Decisions

### Decimal for Financial Data

Used `Decimal` instead of `float` to avoid rounding errors.

---

### Database-Level Aggregation

Used SQL functions instead of Python loops for:

* Performance
* Scalability

---

### Dynamic Query Building

Queries are built dynamically based on user input, ensuring clean and reusable code.

---

### Data Isolation

Each user only accesses their own records using:

```
Record.owner_id == current_user.id
```

---

## Assumptions & Trade-offs

* Authentication is simplified using mock headers (not JWT)
* SQLite is used for simplicity (can be replaced with PostgreSQL)
* Focus is on backend design rather than production deployment

---

## Acknowledgment

This project was built as part of an assignment.
I used official documentation and online resources for guidance, but all code was written, tested, and understood by me.

---

## Conclusion

This project demonstrates:

* Strong backend fundamentals
* Clean architecture
* Efficient database usage
* Role-based access control
* Real-world API design

---

Thank you for reviewing this project!
