# TradeGateway – Unified Order Placement Gateway

## 1. Project Overview

TradeGateway is a Flask-based web application that provides a centralized platform to place and manage orders through multiple broker handlers.

The application supports:

- Angel One
- Zerodha
- Samco
- 5paisa

It provides user registration, login, order placement, order history, dashboard statistics and analytics.

**Important:** The current project runs in MOCK mode. Orders are simulated and do not execute real stock market transactions.

## 2. Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- SQLite
- REST API
- JSON

## 3. Project Structure

```text
TradeGateway/
│
├── brokers/
│   ├── angelone.py
│   ├── zerodha.py
│   ├── samco.py
│   └── fivepaisa.py
│
├── instance/
│   └── orders.db
│
├── logs/
│
├── static/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   └── register.html
│
├── venv/
│
├── app.py
├── config.py
├── database.py
├── order_manager.py
├── requirements.txt
└── .env
```

## 4. Prerequisites

Install the following before running the project:

- Python 3.10 or above
- Visual Studio Code
- Web browser
- Git (optional)

Check Python installation:

```bash
python --version
```

## 5. Installation and Setup

### Step 1: Open the project

Open the TradeGateway folder in Visual Studio Code.

### Step 2: Open the terminal

In VS Code, select:

**Terminal → New Terminal**

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

### Step 4: Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If activation is blocked, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again.

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

If dependencies are not listed in requirements.txt, install:

```bash
pip install Flask python-dotenv
```

### Step 6: Configure environment variables

Create or update the `.env` file in the project root:

```env
SECRET_KEY=replace-with-a-long-random-secret
PORT=5005
```

Use a unique secret key for your own environment. Do not share your `.env` file publicly.

## 6. Run the Application

Execute:

```bash
python app.py
```

The Flask application will start at:

```text
http://127.0.0.1:5005
```

Open the dashboard:

```text
http://127.0.0.1:5005/dashboard
```

## 7. Application URLs

| Page | URL |
|---|---|
| Home | http://127.0.0.1:5005/ |
| Register | http://127.0.0.1:5005/register |
| Login | http://127.0.0.1:5005/login |
| Dashboard | http://127.0.0.1:5005/dashboard |
| Order History | http://127.0.0.1:5005/order-history |
| Dashboard Statistics | http://127.0.0.1:5005/api/dashboard-stats |

The dashboard and API routes require login.

## 8. Main Features

### User Authentication
- User registration
- Secure password hashing
- User login and logout
- Session-based authentication

### Dashboard
- Total orders
- Successful orders
- BUY orders
- SELL orders
- Recent order information
- Broker-wise order overview

### Order Management
- Place BUY and SELL orders
- Select broker
- Enter stock symbol
- Enter quantity
- Select order type
- View order history

### Analytics
- Broker-wise order statistics
- BUY vs SELL distribution
- Success rate
- Dashboard statistics API

## 9. Supported Order Types

- MARKET
- LIMIT
- SL
- SL-M

Supported transaction sides:

- BUY
- SELL

## 10. Sample API Request

**Endpoint:**

```text
POST /place-order
```

**Request Body:**

```json
{
    "broker": "zerodha",
    "symbol": "RELIANCE",
    "qty": 2,
    "side": "BUY",
    "order_type": "MARKET"
}
```

The request must be sent from an authenticated session.

## 11. Database

The application uses SQLite to store:

- User information
- Password hashes
- Order details
- Order history

The database is stored at:

```text
instance/orders.db
```

The application initializes the database when Flask starts.

## 12. Troubleshooting

**Problem: Flask module not found**

```bash
pip install Flask
```

**Problem: dotenv module not found**

```bash
pip install python-dotenv
```

**Problem: Port already in use**

Stop the other Flask process or configure a different port.

**Problem: Dashboard redirects to login**

Register a user or log in first.

**Problem: Charts show zero**

Place some mock orders and refresh the dashboard.

## 13. Future Enhancements

- Live broker API integration
- Advanced order filtering
- User profile management
- Improved analytics
- Deployment to a cloud server
- API token authentication

## 14. Author

**Project Name:** TradeGateway  
**Project Type:** Python Flask Web Application  
**Domain:** Financial Technology / API Integration

---

**TradeGateway – One Gateway, Multiple Brokers.**