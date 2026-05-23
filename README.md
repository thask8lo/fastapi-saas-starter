# ⚡ FastAPI SaaS Boilerplate

A production-ready Python backend starter kit for building SaaS applications fast.
Stop spending days on auth, billing, and project structure — start shipping your product.

---

## ✅ What's Included

| Feature | Details |
|---|---|
| **Authentication** | JWT (access + refresh tokens), register, login, logout |
| **User Management** | Profile CRUD, password update, soft delete |
| **Stripe Billing** | Checkout sessions, subscriptions, webhooks, cancellation |
| **Rate Limiting** | Per-route limits to prevent abuse |
| **Database** | SQLAlchemy ORM, SQLite out of the box, Postgres-ready |
| **Docker** | Dockerfile + docker-compose for instant deployment |
| **Tests** | pytest test suite included |
| **Type Safety** | Full Pydantic v2 schemas |

---

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone https://github.com/thask8lo/fastapi-saas-starter
cd fastapi-saas-starter
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your values
```

Generate a secret key:
```bash
openssl rand -hex 32
```

### 3. Run

```bash
uvicorn app.main:app --reload
```

API docs available at: `http://localhost:8000/docs`

### 4. Run with Docker

```bash
docker-compose up --build
```

---

## 📡 API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Create new account |
| POST | `/api/auth/login` | Login, get tokens |
| POST | `/api/auth/refresh` | Refresh access token |
| POST | `/api/auth/logout` | Logout |

### Users
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/users/me` | Get current user |
| PATCH | `/api/users/me` | Update profile |
| DELETE | `/api/users/me` | Deactivate account |

### Billing
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/billing/create-checkout-session` | Start Stripe checkout |
| GET | `/api/billing/status` | Get subscription status |
| POST | `/api/billing/cancel-subscription` | Cancel at period end |
| POST | `/api/billing/webhook` | Stripe webhook handler |

---

## 💳 Stripe Setup

1. Create a Stripe account at [stripe.com](https://stripe.com)
2. Create a product and a recurring price
3. Copy the Price ID (`price_...`) to your `.env`
4. Set up a webhook pointing to `/api/billing/webhook`
5. Copy the webhook secret to your `.env`

---

## 🐘 Switch to PostgreSQL

1. Uncomment the `db` service in `docker-compose.yml`
2. Update `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql://postgres:postgres@db:5432/saas_db
```

---

## 🧪 Run Tests

```bash
pytest tests/ -v
```

---

## 🌐 Deploy to Render (Free)

1. Push to GitHub
2. Create new Web Service on [render.com](https://render.com)
3. Set environment variables
4. Deploy — free tier available

---

## 🛠️ Tech Stack

- **FastAPI** 0.111 — modern async Python web framework
- **SQLAlchemy** 2.0 — ORM with async support
- **Pydantic** v2 — data validation
- **python-jose** — JWT tokens
- **passlib + bcrypt** — password hashing
- **Stripe** — payments
- **SlowAPI** — rate limiting
- **pytest** — testing
- **Docker** — containerization

---

## 📄 License

MIT — use freely in personal and commercial projects.

---

**Questions?** Open an issue or reach out via Gumroad.
