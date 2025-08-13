# Green Cart 🚚

## 📌 Project Overview
Green Cart is a logistics and delivery management system that optimizes driver assignments, route management, and order scheduling.  
It allows administrators to manage:
- Drivers and their shifts
- Delivery routes with traffic levels
- Orders with delivery times  
The aim is to improve operational efficiency and ensure timely deliveries.

---

## 🛠 Tech Stack

**Frontend**
- React.js
- Axios
- React Router DOM
- Tailwind CSS

**Backend**
- Django
- Django REST Framework
- Django CORS Headers
- djangorestframework-simplejwt
- PostgreSQL
- psycopg2-binary
- argon2-cffi
- pytest-django (for testing)

**Tools**
- Git & GitHub
- Python venv
- Node.js & npm

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

git clone <your-repo-url>
cd green-cart


---

### 2️⃣ Backend Setup


cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

Create a `.env` file in `backend/`:


SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_NAME=green_cart
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432


Run migrations and start the server:


python manage.py migrate
python manage.py runserver


---

### 3️⃣ Frontend Setup


cd ../frontend
npm install
npm start


Create a `.env` file in `frontend/`:


REACT_APP_API_URL=http://localhost:8000/api


---

## 📊 Loading Data from Excel

If you have Excel sheets for **drivers**, **routes**, and **orders**:

* Place them in the `backend/` folder.
* Write a Django management command or script to read them using **pandas** or **openpyxl** and insert into the database.
* Run:


python manage.py shell < load_excel_data.py


---

## 🔑 Environment Variables

**Backend (`backend/.env`):**

SECRET_KEY=
DEBUG=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=


**Frontend (`frontend/.env`):**


REACT_APP_API_URL=

---

## 🚀 Deployment Instructions

**Backend**

* Deploy to Render, Railway, or Heroku.
* Set environment variables in the hosting platform.

**Frontend**

* Deploy to Vercel or Netlify.
* Update `REACT_APP_API_URL` to point to the deployed backend API.

---

## 📡 API Documentation

### Authentication

* **POST** `/api/token/` → Get JWT token.
* **POST** `/api/token/refresh/` → Refresh JWT token.

### Drivers

* **GET** `/api/drivers/` → List all drivers.
* **POST** `/api/drivers/` → Create a new driver.

### Routes

* **GET** `/api/routes/` → List all routes.
* **POST** `/api/routes/` → Create a new route.

### Orders

* **GET** `/api/orders/` → List all orders.
* **POST** `/api/orders/` → Create a new order.

Example:


POST /api/orders/
{
  "order_id": 101,
  "value_rs": 500,
  "route": 1,
  "delivery_time": "15:30"
}

