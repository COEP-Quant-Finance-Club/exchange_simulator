# Exchange Simulator — Phase 2 (Paper Trading Web App)

A real-time paper trading platform built on top of a custom matching engine.
currently the system is only for the one stock.
---

## Phase 2 Detailed Task Checklist

---

## 1. Backend API Layer

- [ ] Set up FastAPI project structure
- [ ] Create main application entry (`main.py`)
- [ ] Initialize matching engine instance
- [ ] Create API route structure (routes folder)
- [ ] Implement `POST /order`
  - [ ] Validate request body
  - [ ] Support LIMIT orders
  - [ ] Support MARKET orders
  - [ ] Pass order to engine
  - [ ] Return execution result
- [ ] Implement `GET /orderbook`
  - [ ] Fetch bids and asks from engine
  - [ ] Format response
- [ ] Implement `GET /trades`
  - [ ] Fetch trade history
  - [ ] Sort by timestamp
- [ ] Implement `GET /portfolio`
  - [ ] Fetch user holdings
  - [ ] Fetch user balance

---

## 2. User Authentication

- [ ] Design User model
- [ ] Implement signup API
  - [ ] Validate input (email/password)
  - [ ] Hash password (bcrypt)
  - [ ] Store user in DB
- [ ] Implement login API
  - [ ] Verify credentials
  - [ ] Generate JWT token
- [ ] Middleware for JWT verification
- [ ] Protect all trading routes
- [ ] Assign initial balance (₹10,00,000)

---

## 3. Database Integration

- [ ] Set up PostgreSQL connection
- [ ] Configure ORM (SQLAlchemy / Prisma equivalent)
- [ ] Create schema:
  - [ ] Users table
  - [ ] Orders table
  - [ ] Trades table
  - [ ] Portfolio table
- [ ] Write migrations
- [ ] Insert initial test data
- [ ] Replace file-based storage with DB operations

---

## 4. Order Management System

- [ ] Define order model fields
  - [ ] id, user_id, type, price, quantity
  - [ ] filled_quantity
  - [ ] status
  - [ ] timestamp
- [ ] Implement order status transitions
- [ ] Update status after each trade execution
- [ ] Handle partial fills correctly
- [ ] Persist order updates in DB

---

## 5. Engine Integration

- [ ] Modify engine to accept user_id
- [ ] Ensure engine returns:
  - [ ] matched trades
  - [ ] remaining quantity
- [ ] Wrap engine calls inside service layer
- [ ] Ensure sequential processing (queue or lock)
- [ ] Handle edge cases:
  - [ ] empty order book
  - [ ] insufficient liquidity

---

## 6. Portfolio & Balance Management

- [ ] Design portfolio schema
- [ ] Implement balance tracking per user
- [ ] On BUY execution:
  - [ ] Deduct balance
  - [ ] Increase stock quantity
- [ ] On SELL execution:
  - [ ] Increase balance
  - [ ] Decrease stock quantity
- [ ] Maintain average price calculation
- [ ] Implement P&L calculation
  - [ ] Realized P&L
  - [ ] Unrealized P&L

---

## 7. Real-Time System (WebSockets)

- [ ] Set up WebSocket endpoint
- [ ] Manage connected clients list
- [ ] Broadcast events:
  - [ ] Order book updates
  - [ ] Trade execution updates
- [ ] Handle client disconnects
- [ ] Optimize message payloads

---

## 8. Frontend Application (React)

### Setup
- [ ] Initialize React app (Vite / Next.js)
- [ ] Set up routing
- [ ] Configure API base URL

### Authentication UI
- [ ] Signup page
- [ ] Login page
- [ ] Store JWT token (secure storage)

### Dashboard Page
- [ ] Display balance
- [ ] Display portfolio holdings
- [ ] Display P&L

### Trading Page
- [ ] Create Buy/Sell form
- [ ] Add order type selector (LIMIT / MARKET)
- [ ] Conditional price input
- [ ] Submit order to backend
- [ ] Display live order book
- [ ] Display recent trades
- [ ] Connect to WebSocket for live updates

### History Page
- [ ] Display order history
- [ ] Display trade history

---

## 9. Multi-User Support

- [ ] Ensure multiple users can log in simultaneously
- [ ] Handle concurrent order submissions
- [ ] Prevent race conditions
- [ ] Validate ownership of orders

---

## 10. Deployment

- [ ] Prepare environment variables
- [ ] Deploy backend (Render / Railway)
- [ ] Deploy frontend (Vercel)
- [ ] Connect frontend to deployed backend
- [ ] Test production endpoints

---

## 11. Testing & Validation

- [ ] Unit test engine integration
- [ ] Test order placement flow
- [ ] Test matching scenarios
- [ ] Test portfolio updates
- [ ] Test multi-user trading
- [ ] Test WebSocket updates

---

## Definition of Done

- [ ] User can sign up and log in
- [ ] User can place LIMIT and MARKET orders
- [ ] Orders are matched automatically
- [ ] Trades are stored and visible
- [ ] Portfolio updates correctly
- [ ] Real-time updates are working
- [ ] Application is deployed and accessible