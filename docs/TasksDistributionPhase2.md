# Exchange Simulator — Phase 2 Task Distribution (Single Stock)

## Phase 2 Goal

Build a **Real-Time Paper Trading System** for **Single Stock**

Features:
- User Authentication
- Order Placement (LIMIT / MARKET)
- Matching Engine Integration
- Portfolio Tracking
- Real-time updates
- Multi-user support

---

# Team Members

- Bhavesh — Engine Integration + Order Management + Core Logic
- Ved Bajaj — Backend Architecture + Database + Authentication
- Shreyas — Frontend (React)
- Shreya K — FastAPI Routes
- Arnav  — WebSocket + Real-Time Updates
- Member 6 — Testing + QA
- Member 7 — Documentation + Deployment

---

# 1. Bhavesh — Engine Integration + Order Management

## Engine Integration

- [ ] Initialize matching engine in backend
- [ ] Connect API to engine
- [ ] Handle trade execution response
- [ ] Handle remaining quantity

---

## Order Management

- [ ] Define order model
- [ ] Order status (OPEN / PARTIAL / FILLED)
- [ ] Handle partial fills
- [ ] Update order after trade execution

---

## Portfolio Logic

- [ ] Update portfolio on BUY
- [ ] Update portfolio on SELL
- [ ] Update user balance
- [ ] Calculate average price

---

## Multi User Support

- [ ] Handle concurrent orders
- [ ] Prevent race conditions
- [ ] Validate order ownership

---

# 2. Ved Bajaj — Backend Architecture + Database + Auth

## Backend Setup

- [ ] Setup FastAPI project
- [ ] Create main.py
- [ ] Create routes folder
- [ ] Initialize engine instance

---

## Database Setup

- [ ] Setup PostgreSQL / Supabase
- [ ] Configure ORM (SQLAlchemy) (object relational mapping)

---

## Database Schema

- [ ] Users table
- [ ] Orders table
- [ ] Trades table
- [ ] Portfolio table

---

## Authentication (Bhavesh will also help)

- [ ] Signup API
- [ ] Login API
- [ ] Password hashing
- [ ] JWT authentication

---

## User Balance

- [ ] Assign ₹15,00,000 initial balance

---

# 3. Shreyas — Frontend (React)

## Setup

- [ ] Initialize React app
- [ ] Setup routing
- [ ] Configure API base URL

---

## Authentication UI

- [ ] Signup page
- [ ] Login page

---

## Dashboard

- [ ] Display balance
- [ ] Display holdings
- [ ] Display P&L

---

## Trading Page

- [ ] Buy/Sell form
- [ ] LIMIT / MARKET selector
- [ ] Price input
- [ ] Quantity input
- [ ] Submit order

---

## Orderbook

- [ ] Display bids
- [ ] Display asks

---

## Trades

- [ ] Display recent trades

---

## WebSocket

- [ ] Connect WebSocket
- [ ] Update UI in real-time

---

# 4. Shreya K — FastAPI Routes 

## Setup

- [ ] Create backend/routes folder

Files:

- [ ] orders.py
- [ ] orderbook.py
- [ ] trades.py
- [ ] portfolio.py

---

## Order API

- [ ] POST `/order`
- [ ] Validate request
- [ ] Send order to engine
- [ ] Return execution result

---

## Orderbook API

- [ ] GET `/orderbook`
- [ ] Fetch bids
- [ ] Fetch asks

---

## Trades API

- [ ] GET `/trades`
- [ ] Fetch trade history
- [ ] Sort by timestamp

---

## Portfolio API

- [ ] GET `/portfolio`
- [ ] Fetch holdings
- [ ] Fetch balance

---

# 5. Arnav — WebSocket + Real-Time

## WebSocket Setup

- [ ] Create WebSocket endpoint
- [ ] Manage connected clients

---

## Real-Time Events

- [ ] Broadcast orderbook updates
- [ ] Broadcast trade execution
- [ ] Broadcast portfolio updates

---

## Connection Handling

- [ ] Handle client connect
- [ ] Handle disconnect
- [ ] Optimize payload

---

# 6. Member 6 — Testing + QA

## Engine Testing

- [ ] Test LIMIT orders
- [ ] Test MARKET orders
- [ ] Test partial fills

---

## API Testing

- [ ] Test signup
- [ ] Test login
- [ ] Test order placement

---

## Portfolio Testing

- [ ] Test BUY execution
- [ ] Test SELL execution
- [ ] Test balance update

---

## Multi-user Testing

- [ ] Multiple users trading
- [ ] Concurrent order placement

---

# 7. Member 7 — Documentation + Deployment

## Documentation

- [ ] Update README.md
- [ ] API documentation
- [ ] Folder structure documentation

---


## Final Testing

- [ ] Test deployed backend
- [ ] Test frontend connection
- [ ] Fix deployment issues

---

# Phase 2 Definition of Done

- [ ] User signup/login works
- [ ] LIMIT orders work
- [ ] MARKET orders work
- [ ] Matching engine works
- [ ] Portfolio updates correctly
- [ ] Real-time updates working
- [ ] Multi-user support working
- [ ] Application deployed

---

# Phase 2 Architecture

Frontend (React)
        |
FastAPI Backend
        |
Matching Engine
        |
    Database

the backend, frontend and websocket person will work together.