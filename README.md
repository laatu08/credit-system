
# Credit Approval System – Backend

This repository contains the backend implementation of a **Credit Approval System** built using **Django**, **Django REST Framework**, **PostgreSQL**, **Celery**, **Redis**, and **Docker**.

The system evaluates customer creditworthiness based on historical loan data, applies credit score rules, checks loan eligibility, and supports loan creation via REST APIs.

---

## 🚀 Tech Stack

- **Backend Framework:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Async Tasks:** Celery + Redis
- **Containerization:** Docker & Docker Compose

---

## 🧠 Core Features

- Customer registration via API
- Credit score calculation using historical loan data
- Loan eligibility checks with interest rate correction logic
- Loan creation and retrieval APIs
- Asynchronous ingestion of initial customer and loan data
- Clean separation of business logic using a service layer
- Fully containerized and reproducible setup

---

## 📁 Project Structure

```
credit-system/
├── core/
│   ├── models.py              # Customer and Loan models
│   ├── services/              # Credit score & eligibility logic
│   ├── views/                 # API views
│   ├── serializers/           # DRF serializers
│   ├── tasks/                 # Celery background tasks
│   ├── management/commands/   # Custom Django commands
│   └── migrations/            # Database migrations
├── credit_system/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/laatu08/credit-system.git
cd credit-system
```

---

### 2️⃣ Start the Application (Docker)

Make sure Docker and Docker Compose are installed.

```bash
docker-compose up --build
```

This will start:
- Django web server
- PostgreSQL database
- Redis
- Celery worker

---

### 3️⃣ Apply Database Migrations

```bash
docker-compose exec web python manage.py migrate
```

---

### 4️⃣ Create Superuser (Admin Access)

```bash
docker-compose exec web python manage.py createsuperuser
```

Access admin panel at:
```
http://localhost:8000/admin/
```

---

## 📊 Data Ingestion (Important)

Initial customer and loan data is ingested asynchronously using **Celery**.

### Run Ingestion Command

```bash
docker-compose exec web python manage.py ingest_initial_data
```

This command:
- Submits background jobs to Celery
- Loads customer and loan data from Excel files
- Does not block the API server

> ⚠️ Note: Excel files are intentionally **not committed** to the repository.  
> The system is designed to work with external data sources.

---

## 🔗 API Endpoints

### 1️⃣ Register Customer
**POST** `/api/register/`

```json
{
  "first_name": "Rohit",
  "last_name": "Verma",
  "age": 28,
  "monthly_salary": 50000,
  "phone_number": 9876543210
}
```

**Response**
```json
{
  "customer_id": 12,
  "approved_limit": 1800000,
  "message": "Customer registered successfully"
}
```

---

### 2️⃣ Check Loan Eligibility
**POST** `/api/check-eligibility/`

```json
{
  "customer_id": 12,
  "loan_amount": 300000,
  "interest_rate": 10,
  "tenure": 18
}
```

---

### 3️⃣ Create Loan
**POST** `/api/create-loan/`

---

### 4️⃣ View Loan by ID
**GET** `/api/view-loan/{loan_id}/`

---

### 5️⃣ View All Loans for a Customer
**GET** `/api/view-loans/{customer_id}/`

---

## 🧮 Credit Logic Summary

- Credit score calculated out of **100**
- Based on:
  - EMIs paid on time
  - Number of loans taken
  - Loan activity in the current year
  - Total loan exposure vs approved limit
- Loan approval rules:
  - Credit score > 50 → approved
  - 30 < score ≤ 50 → approved only if interest > 12%
  - 10 < score ≤ 30 → approved only if interest > 16%
  - Score ≤ 10 → rejected
  - EMI burden > 50% salary → rejected
- If interest does not match slab, corrected interest is returned

---

## 🧪 API Documentation

Postman documentation:
```
https://documenter.getpostman.com/view/33307977/2sBXVo87nx
```

---

## 🎥 Video Demo

YouTube walkthrough:
```
https://youtu.be/We92XCvdXNM
```

---

## 📌 Notes

- Database schema managed via Django migrations
- Excel files excluded intentionally
- External customer IDs used only for ingested data
- API-registered customers rely on internal primary keys

---

## 👤 Author

**Partha Borah**

---

## ✅ Status

✔ Assignment completed as per requirements  
✔ GitHub repository and video demo submitted  

