# 📦 Smart Emergency Warehouse Management & Relief Distribution System

**A comprehensive, extensible MVP for managing emergency supplies, warehouse inventory, and relief distribution operations.**

Designed and developed independently by **Vida Khoshpey**.

This project aims to provide a structured and practical solution for managing emergency warehouse operations, covering the complete inventory lifecycle:

**Receiving → Storage → Allocation → Distribution**

It focuses on inventory accuracy, operational traceability, role-based access control, and efficient resource distribution.

Rather than being a simple inventory tracker, the system provides a modular foundation for managing warehouse workflows, tracking inventory movements, organizing distribution missions, and generating operational reports.

> **Project status:** Independently developed MVP. Open to improvements, contributions, feature extensions, and community feedback.

---

## ✨ Key Features

- **Inventory Management:** Manage products, stock quantities, warehouse locations, and inventory batches.
- **Batch Tracking:** Track expiration dates, batch numbers, and storage locations.
- **FEFO Support:** Structure inventory operations around the First Expired, First Out principle.
- **Emergency Distribution:** Create and manage distribution missions and allocate supplies.
- **Inventory Transactions:** Record receiving, allocation, issuing, transfers, and stock adjustments.
- **Role-Based Access Control (RBAC):** Separate permissions for administrators, operators, and warehouse staff.
- **Audit Trail:** Maintain records of important operational changes.
- **Reporting:** Monitor current stock, low-stock items, expiring batches, and inventory turnover.
- **RESTful API:** Provide structured API endpoints through FastAPI.
- **Containerization:** Support deployment through Docker Compose.
- **Database Migrations:** Use Alembic to manage database schema changes.

## 🏗️ Architecture

The application follows a layered architecture to improve maintainability, separation of concerns, and future extensibility.

```text
┌──────────────────────────────────────────────┐
│                 Frontend                     │
│              React + Axios                   │
│                                              │
│  Pages → Auth Context → API Client           │
└──────────────────────┬───────────────────────┘
                       │ HTTP / JSON
┌──────────────────────▼───────────────────────┐
│                 Backend                      │
│                 FastAPI                      │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │ API Layer                              │  │
│  │ Routes, Validation, Authentication     │  │
│  └────────────────────┬───────────────────┘  │
│                       │                      │
│  ┌────────────────────▼───────────────────┐  │
│  │ Service Layer                          │  │
│  │ Inventory & Reporting Business Logic  │  │
│  └────────────────────┬───────────────────┘  │
│                       │                      │
│  ┌────────────────────▼───────────────────┐  │
│  │ Data Layer                             │  │
│  │ SQLAlchemy ORM Models                  │  │
│  └────────────────────┬───────────────────┘  │
└───────────────────────┼──────────────────────┘
                        │
               ┌────────▼────────┐
               │   PostgreSQL    │
               └─────────────────┘
```

### Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | React |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Data Validation | Pydantic |
| Database Migrations | Alembic |
| HTTP Client | Axios |
| Deployment | Docker, Docker Compose |
| Web Server | Nginx |

---

## 📁 Project Structure

```text
warehouse-project/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── inventory_service.py
│   │   │   └── report_service.py
│   │   ├── api/
│   │   │   ├── deps.py
│   │   │   └── routes/
│   │   ├── main.py
│   │   └── seed.py
│   ├── alembic/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── context/
│   │   ├── components/
│   │   └── pages/
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

---

## 🗄️ Database Design

One of the main design considerations is the separation between a product and its physical inventory batches.

An `Item` represents a product definition, while a `Batch` represents an actual quantity of that product stored at a particular location, potentially with its own expiration date and batch number.

This separation enables more accurate inventory tracking and supports expiration-aware stock allocation.

### Main Entities

| Entity | Responsibility |
|---|---|
| Users | System accounts and access roles |
| Items | Product definitions and SKU information |
| Locations | Physical warehouse storage locations |
| Batches | Actual inventory quantities and expiration data |
| Missions | Emergency distribution requests |
| Transactions | Inventory movement ledger |
| Audit Logs | Records of important system changes |

---

## 🔄 Core Warehouse Workflow

The system is organized around five primary inventory operations.

### 1. Receiving
Register incoming supplies and add them to warehouse inventory.

`POST /api/transactions/receive`

### 2. Allocation
Reserve available quantities for a specific distribution mission without immediately reducing physical stock.

`POST /api/transactions/allocate`

### 3. Issuing & Distribution
Record the actual release and delivery of supplies.

`POST /api/transactions/issue`

### 4. Stock Transfer
Move inventory between warehouse locations.

`POST /api/transactions/transfer`

### 5. Stock Adjustment
Correct inventory discrepancies based on physical stock counts.

`POST /api/transactions/adjust`

These operations are designed to maintain transaction history and improve inventory traceability.

---

## 🔐 Roles & Permissions

The application supports three primary roles:

| Role | Access |
|---|---|
| Admin | Full system management, user administration, inventory adjustments, and reporting |
| Operator | Product and location management, inventory operations, and distribution missions |
| Warehouse Staff | Physical receiving and issuing operations |

Access control is handled at the API layer rather than relying solely on frontend restrictions.

---

## 🚀 Getting Started

### Prerequisites

- Docker
- Docker Compose
- Git

For manual installation:

- Python
- Node.js and npm
- PostgreSQL

### Installation with Docker

Clone the repository:

```bash
git clone git@github.com:VIDAKHOSHPEY22/warehouse_project.git

cd warehouse_project
```

Configure environment variables:

```bash
cp backend/.env.example backend/.env
```

Review the environment configuration and update sensitive values before starting the application.

Build and start the services:

```bash
docker compose up -d --build
```

Initialize the database and seed initial data:

```bash
docker compose exec backend python -m app.seed
```

### Access the Application

| Service | URL |
|---|---|
| Frontend | http://localhost |
| Backend API | http://localhost:8000 |
| Interactive API Documentation | http://localhost:8000/docs |

**Important:** If the seed process creates a default administrator account, change its initial password immediately. Never use development credentials in a public deployment.

---

## 🧩 API Overview

The application provides RESTful endpoints for authentication, inventory management, warehouse locations, distribution missions, transactions, and reporting.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/login` | User authentication |
| GET | `/api/auth/me` | Current user information |
| GET / POST | `/api/items` | List and create products |
| GET / POST | `/api/locations` | List and create locations |
| GET | `/api/batches` | Retrieve inventory batches |
| GET / POST | `/api/missions` | Manage distribution missions |
| POST | `/api/transactions/receive` | Receive supplies |
| POST | `/api/transactions/allocate` | Allocate inventory |
| POST | `/api/transactions/issue` | Issue supplies |
| POST | `/api/transactions/transfer` | Transfer stock |
| POST | `/api/transactions/adjust` | Adjust inventory |
| GET | `/api/reports/current-stock` | Current inventory report |
| GET | `/api/reports/low-stock` | Low-stock report |
| GET | `/api/reports/expiring-batches` | Expiration report |
| GET | `/api/reports/turnover` | Inventory turnover report |

For the complete interactive API reference, visit `/docs` after starting the backend.

---

## 🛣️ Future Development

This project is designed to be extensible. Potential improvements include:

- Barcode and QR code generation and scanning.
- Advanced inventory analytics and visualization.
- Expanded automated test coverage.
- Enhanced offline operation and data synchronization.
- Automated database backups and recovery.
- Additional warehouse and distribution workflows.
- Further security and deployment improvements.

These are potential development directions, not claims that every feature is already implemented.

---

## 🔒 Security & Production Considerations

Before deploying this project in a production environment:

- Generate a strong and unique `SECRET_KEY`.
- Change all default credentials.
- Store sensitive configuration in environment variables.
- Restrict CORS origins to trusted domains.
- Enable HTTPS.
- Secure database credentials and Docker configuration.
- Configure automated database backups.
- Review authentication, authorization, and audit logging.
- Run appropriate automated and integration tests.

This repository represents an MVP and should undergo security review and deployment validation before handling real emergency or humanitarian operations.

---

## 🤝 Contributions & Community

This project was independently designed and developed by me, and I am happy to share it with the developer community.

I consider this project an evolving foundation rather than a closed implementation.

**I would genuinely appreciate your feedback, suggestions, improvements, and contributions.**

Whether you find a bug, identify an architectural improvement, suggest a new feature, or want to improve the existing implementation, your contribution is welcome.

Feel free to:

- Open an issue.
- Submit a pull request.
- Suggest new features.
- Improve documentation.
- Share ideas for making the system more reliable and useful.

I would be happy to see the project improved and updated through community collaboration.

---

## 👩‍💻 Author

**Vida Khoshpey**

Independent Developer | Programming Instructor | Founder of Dumirror

- GitHub: [@VIDAKHOSHPEY22](https://github.com/VIDAKHOSHPEY22)

---

## ⭐ Support the Project

If you find this project useful, consider giving it a star ⭐

Your feedback and contributions help make it better.

**Built independently with a focus on practical software engineering, maintainable architecture, and meaningful real-world applications.**
